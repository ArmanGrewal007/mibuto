#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
GRAY='\033[90m'
ORANGE='\033[33m'

# Text formatting 
BOLD="\033[1m"
NEGATIVE_INTENSITY="\033[2m"
ITALICS="\033[3m"
UNDERLINE="\033[4m"
BLINKING="\033[5m"
POSITIVE_INTESTITY="\033[6m"
INVERTED="\033[7m"
HIDDEN="\033[8m"
STRIKETHROUGH="\033[9m"

# Configuration
# Get the current IP address
get_ip_address() {
    if command -v ip &> /dev/null; then
        # Linux with 'ip' command
        IP=$(ip route get 1 | awk '{print $7;exit}')
    elif command -v ifconfig &> /dev/null; then
        # macOS or Linux with 'ifconfig'
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
        else
            # Linux with ifconfig
            IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -n 1)
        fi
    else
        # Fallback to localhost if no command works
        IP="127.0.0.1"
        echo "Warning: Could not detect IP address, using localhost"
    fi
    echo $IP
}
BASE_URL="http://$(get_ip_address):5001"
ADMIN_USERNAME="arman"
ADMIN_PASSWORD="arman"
TEST_USERNAME="testuser"
TEST_EMAIL="test@example.com"
TEST_PASSWORD="testpass"

# Test counters
PASSED=0
FAILED=0
TOKEN=""

# Array to store failed commands
declare -a FAILED_COMMANDS
declare -a FAILED_TEST_NAMES

# Helper function for making HTTP requests
make_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local use_auth=${4:-false}
    
    local auth_header=""
    if [ "$use_auth" = true ] && [ ! -z "$TOKEN" ]; then
        auth_header="-H \"Authorization: Bearer $TOKEN\""
    fi
    
    local curl_cmd="curl -s -w \"\n%{http_code}\" -X $method \
        -H \"Content-Type: application/json\" \
        $auth_header \
        ${data:+-d '$data'} \
        $BASE_URL$endpoint"
        
    LAST_CURL_CMD="$curl_cmd"
    response=$(eval $curl_cmd)
    http_code=$(echo "$response" | tail -n1)
    content=$(echo "$response" | sed '$d')
}

# Helper function for validating responses
validate_response() {
    local test_name=$1
    local expected_code=$2
    local expected_content=$3
    
    if [[ $http_code -eq $expected_code && $content == *"$expected_content"* ]]; then
        print_result 0 "$test_name"
        return 0
    else
        print_result 1 "$test_name"
        FAILED_COMMANDS+=("$LAST_CURL_CMD")
        FAILED_TEST_NAMES+=("$test_name")
        return 1
    fi
}

# Function to print test results
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "$2 ${GREEN}✓ PASSED${NC}"
        PASSED=$((PASSED + 1))
    else
        echo -e "$2 ${RED}✗ FAILED${NC}"
        FAILED=$((FAILED + 1))
    fi
}

# Function to run a test section
run_section() {
    local section_name=$1
    echo -e "\n${GRAY}Starting $section_name Tests...${NC}"
}

# User Management Tests
run_user_tests() {
    run_section "User"

    # Test user registration with valid data
    local signup_data="{\"username\": \"$TEST_USERNAME\", \"password\": \"$TEST_PASSWORD\", \"full_name\": \"Test User\", \"qualification\": \"BSc\", \"dob\": \"2000-01-01\"}"
    make_request "POST" "/user-signup" "$signup_data"
    validate_response "User Registration" 201 "User registered successfully"

    # Test duplicate registration (should fail)
    make_request "POST" "/user-signup" "$signup_data"
    validate_response "Duplicate User Registration" 400 "Username is already taken"

    # Test valid user login
    local login_data="{\"username\": \"$TEST_USERNAME\", \"password\": \"$TEST_PASSWORD\"}"
    make_request "POST" "/user-login" "$login_data"
    if validate_response "User Login" 200 "Login successful"; then
        USER_TOKEN=$(echo "$content" | jq -r '.token')  # Correct token field
        echo -e "${GRAY}User token obtained successfully${NC}"
    fi

    # Test invalid login credentials
    local invalid_login_data="{\"username\": \"$TEST_USERNAME\", \"password\": \"wrongpass\"}"
    make_request "POST" "/user-login" "$invalid_login_data"
    validate_response "Invalid Login" 401 "Invalid username or password"
}

# Admin Tests
run_admin_tests() {
    run_section "Admin"
    
    # Admin login with credentials from create-admin command
    local admin_login_data="{\"username\": \"$ADMIN_USERNAME\", \"password\": \"$ADMIN_PASSWORD\"}"
    make_request "POST" "/admin-login" "$admin_login_data"
    
    if validate_response "Admin Login" 200 "Login successful"; then
        # Extract token from correct field in response
        TOKEN=$(echo "$content" | jq -r '.token')
        echo -e "${GRAY}Admin token obtained successfully${NC}"
    else
        echo -e "${RED}Cannot proceed with admin tests without valid admin token.${NC}"
        echo -e "${YELLOW}Make sure to first run: flask create-admin <username> <password> <full_name> <qualification> <dob>${NC}"
        return 1
    fi
}

# Subject Management Tests
run_subject_tests() {
    run_section "Subject"
    
    # Test subject creation
    local subject_data="{\"name\": \"Mathematics\", \"description\": \"Advanced mathematics courses\"}"
    make_request "POST" "/create-subject" "$subject_data" true
    validate_response "Create Subject" 201 "Subject created successfully"
    
    # Get the subject ID from the response for later use
    SUBJECT_ID=$(echo $content | jq -r '.subject.id')
    
    # Test duplicate subject creation
    make_request "POST" "/create-subject" "$subject_data" true
    validate_response "Duplicate Subject Creation" 409 "already exists"
    
    # Test create subject without name
    local invalid_subject_data="{\"description\": \"Invalid subject\"}"
    make_request "POST" "/create-subject" "$invalid_subject_data" true
    validate_response "Create Subject Without Name" 400 "Subject name is required"
    
    # Test create subject without authentication
    make_request "POST" "/create-subject" "$subject_data" false
    validate_response "Create Subject Without Auth" 401 "Missing Authorization Header"
    
    # Test get all subjects
    make_request "GET" "/get-subject"
    validate_response "Get All Subjects" 200 "Mathematics"
    
    # Test get specific subject
    make_request "GET" "/get-subject?id=$SUBJECT_ID"
    validate_response "Get Specific Subject" 200 "Mathematics"
    
    # Test get non-existent subject
    make_request "GET" "/get-subject?id=999999"
    validate_response "Get Non-existent Subject" 404 "Subject not found"
    
    # Test update subject
    local update_data="{\"subject_id\": $SUBJECT_ID, \"name\": \"Advanced Mathematics\", \"description\": \"Updated description\"}"
    make_request "PATCH" "/update-subject/$SUBJECT_ID" "$update_data" true
    validate_response "Update Subject" 200 "Subject updated successfully"
    
    # Test update subject without authentication
    make_request "PATCH" "/update-subject/$SUBJECT_ID" "$update_data" false
    validate_response "Update Subject Without Auth" 401 "Missing Authorization Header"
    
    # Test update non-existent subject
    local invalid_update_data="{\"subject_id\": 999999, \"name\": \"Invalid Update\"}"
    make_request "PATCH" "/update-subject/999999" "$invalid_update_data" true
    validate_response "Update Non-existent Subject" 404 "Subject not found"
    
    # Test update subject with duplicate name
    local second_subject_data="{\"name\": \"Physics\", \"description\": \"Physics courses\"}"
    make_request "POST" "/create-subject" "$second_subject_data" true
    local second_subject_id=$(echo $content | jq -r '.subject.id')
    
    local duplicate_name_data="{\"subject_id\": $second_subject_id, \"name\": \"Advanced Mathematics\"}"
    make_request "PATCH" "/update-subject/$second_subject_id" "$duplicate_name_data" true
    validate_response "Update Subject with Duplicate Name" 409 "already exists"
    
    # Test delete subject
    make_request "DELETE" "/delete-subject/$second_subject_id" "" true
    validate_response "Delete Subject" 200 "Subject deleted successfully"
    
    # Test delete subject without authentication
    make_request "DELETE" "/delete-subject/$SUBJECT_ID" "" false
    validate_response "Delete Subject Without Auth" 401 "Missing Authorization Header"
    
    # Test delete non-existent subject
    make_request "DELETE" "/delete-subject/999999" "" true
    validate_response "Delete Non-existent Subject" 404 "Subject not found"
    
    # Clean up - delete the remaining test subject
    make_request "DELETE" "/delete-subject/$SUBJECT_ID" "" true
}

print_summary() {
    echo -e "\n${GRAY}${BOLD}${UNDERLINE}Test Summary:${NC}"
    echo -e "${GREEN}Passed: $PASSED${NC}"
    echo -e "${RED}Failed: $FAILED${NC}"
    echo -e "${ORANGE}Total: $((PASSED + FAILED))${NC}"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "\n${GREEN}Woooohoooo 🎉🎉🎉${NC}"
    fi
    
    if [ ${#FAILED_COMMANDS[@]} -gt 0 ]; then
        echo -e "\n${RED}${BOLD}${UNDERLINE}Failed Test Commands:${NC}"
        for i in "${!FAILED_COMMANDS[@]}"; do
            echo -e "${RED}Test: ${FAILED_TEST_NAMES[$i]}${NC}"
            echo -e "${FAILED_COMMANDS[$i]}"
        done
    fi
}

run_user_tests
run_admin_tests
run_subject_tests

print_summary