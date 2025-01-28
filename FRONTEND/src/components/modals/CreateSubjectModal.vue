<!-- CreateSubjectModal.vue -->
<template>
    <div class="modal show d-block" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content modal-custom">
                <div class="text-center modal-header">
                    <h5 class="modal-title">Create New Subject</h5>
                    <button type="button" class="btn-close" @click="$emit('close')"></button>
                </div>

                <div class="modal-body">
                    <form @submit.prevent="handleSubmit">
                        <div class="row g-3">
                            <!-- Subject Name -->
                            <div class="form-floating col-md-6">
                                <input id="theater-name" v-model="formData.name" placeholder="" class="form-control" />
                                <label for="theater-name" class="form-label">Name<span
                                        class="text-danger">*</span></label>
                            </div>

                            <!-- Total Capacity -->
                            <div class="form-floating col-md-6">
                                <input id="total-capacity" v-model="formData.total_capacity" placeholder=""
                                    type="number" required class="form-control" />
                                <label for="total-capacity" class="form-label">Total Capacity<span
                                        class="text-danger">*</span></label>
                            </div>

                            <!-- Screen Count -->
                            <div class="form-floating col-md-6">
                                <input id="screen-count" v-model="formData.screen_count" placeholder="" type="number"
                                    required class="form-control" />
                                <label for="screen-count" class="form-label">Screen Count</label>
                            </div>

                            <!-- City Selection -->
                            <div class="form-floating col-md-6">
                                <select id="city" v-model="formData.city_id" placeholder="" class="form-select">
                                    <option value="">Select City</option>
                                    <option v-for="city in cities" :key="city.id" :value="city.id">
                                        {{ city.name }}
                                    </option>
                                </select>
                                <label v-if="formData.city_id" for="city" class="form-label">City<span
                                        class="text-danger">*</span></label>
                            </div>
                            <!-- Amenities -->
                            <div class="form-floating col-md-12">
                                <textarea id="amenities" v-model="formData.amenities" placeholder=""
                                    class="form-control"></textarea>
                                <label for="amenities" class="form-label">Amenities (JSON format)</label>
                            </div>
                        </div>
                    </form>
                    <div class="mt-3 small text-white text-end">
                        <em><span class="text-danger">*</span> These fields are required</em>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" @click="randomizeFields" class="btn btn-info">
                        Randomize Fields
                    </button>
                    <button type="button" @click="clearFields" class="btn btn-secondary">
                        Clear
                    </button>
                    <button type="button" @click="$emit('close')" class="btn btn-secondary">
                        Cancel
                    </button>
                    <button type="submit" @click="handleSubmit" class="btn btn-success" :disabled="!isFormValid">
                        Create Subject
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div class="modal-backdrop show"></div>
</template>

<script>
import { ref, computed } from 'vue';
import { faker } from '@faker-js/faker';
import { useStore } from 'vuex';

export default {
    name: 'CreateSubjectModal',
    emits: ['close', 'submit'],
    setup(props, { emit }) {
        const formData = ref({
            name: '',
            total_capacity: '',
            screen_count: 1,
            amenities: '{"WiFi": true}',
            city_id: ''
        });

        const store = useStore();
        const cities = computed(() => store.getters['cities/getCities']);

        const isFormValid = computed(() => {
            return formData.value.name && formData.value.total_capacity && formData.value.city_id;
        });

        const randomizeFields = () => {
            if (cities.value.length === 0) {
                console.warn('No cities available to randomize.');
                return;
            }

            const randomCity = cities.value[Math.floor(Math.random() * cities.value.length)];

            formData.value = {
                name: faker.company.name(),
                total_capacity: faker.number.int({ min: 50, max: 1000 }),
                screen_count: faker.number.int({ min: 1, max: 10 }),
                amenities: JSON.stringify({
                    WiFi: faker.datatype.boolean(),
                    PARKING: faker.datatype.boolean(),
                    AC: faker.datatype.boolean()
                }),
                city_id: randomCity ? randomCity.id : ''
            };
        };


        const clearFields = () => {
            formData.value = {
                name: '',
                total_capacity: '',
                screen_count: 1,
                amenities: '{}',
                city_id: ''
            };
        };

        const handleSubmit = () => {
            const selectedCity = cities.value.find(city => city.id === formData.value.city_id);
            let amenitiesJson;
            try {
                amenitiesJson = JSON.parse(formData.value.amenities);
            } catch {
                amenitiesJson = {};
            }
            emit('submit', {
                ...formData.value,
                city_name: selectedCity ? selectedCity.name : null,
                amenities: amenitiesJson
            });
        };

        return {
            formData,
            randomizeFields,
            cities,
            clearFields,
            handleSubmit,
            isFormValid
        };
    }
};
</script>

<style src="./modalStyle.css" scoped></style>