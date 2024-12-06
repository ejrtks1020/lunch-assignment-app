'use client';


import { useSelector, useDispatch } from 'react-redux';
import { 
  fetchRestaurants, 
  searchRestaurants, 
  getRestaurantById,
  setFilter 
} from '@/store/slices/restaurantSlice';

export const useRestaurant = () => {
  const dispatch = useDispatch();
  const { restaurants, loading, selectedRestaurant, filter, error } = useSelector(
    (state) => state.restaurant
  );

  const handleFetchRestaurants = async () => {
    try {
      await dispatch(fetchRestaurants()).unwrap();
    } catch (error) {
      console.error('레스토랑 데이터를 불러오는데 실패했습니다:', error);
    }
  };

  const handleSearchRestaurants = async (query) => {
    try {
      await dispatch(searchRestaurants(query)).unwrap();
    } catch (error) {
      console.error('레스토랑 검색에 실패했습니다:', error);
    }
  };

  const handleGetRestaurantById = async (id) => {
    try {
      await dispatch(getRestaurantById(id)).unwrap();
    } catch (error) {
      console.error('레스토랑 상세 정보를 불러오는데 실패했습니다:', error);
    }
  };

  const handleSetFilter = (filterData) => {
    dispatch(setFilter(filterData));
  };

  return {
    restaurants,
    loading,
    selectedRestaurant,
    filter,
    error,
    fetchRestaurants: handleFetchRestaurants,
    searchRestaurants: handleSearchRestaurants,
    getRestaurantById: handleGetRestaurantById,
    setFilter: handleSetFilter,
  };
}; 