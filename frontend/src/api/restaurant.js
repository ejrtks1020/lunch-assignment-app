import apiClient from '@/lib/axios';

export const restaurantAPI = {
  // 레스토랑 목록 조회
  getRestaurants: async () => {
    const response = await apiClient.get('/restaurant');
    return response.data;
  },

  // 레스토랑 상세 조회
  getRestaurantById: async (id) => {
    const response = await apiClient.get(`/restaurant/${id}`);
    return response.data;
  },

  // 레스토랑 검색
  searchRestaurants: async (query) => {
    const response = await apiClient.get('/restaurant/search', { params: { query } });
    return response.data;
  }
}; 