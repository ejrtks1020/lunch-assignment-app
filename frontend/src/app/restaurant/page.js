'use client';

import { useEffect } from 'react';
import styles from './restaurant.module.css';
import { useRestaurant } from '@/hooks/useRestaurant';

export default function RestaurantPage() {
  const { 
    restaurants, 
    loading, 
    filter, 
    setFilter, 
    fetchRestaurants, 
    searchRestaurants,
    error 
  } = useRestaurant();

  useEffect(() => {
    fetchRestaurants();
  }, []);

  const handleSearch = (e) => {
    const query = e.target.value;
    setFilter({ search: query });
    if (query) {
      searchRestaurants(query);
    } else {
      fetchRestaurants();
    }
  };

  if (loading) {
    return <div className={styles.loading}>로딩 중...</div>;
  }

  if (error) {
    return <div className={styles.error}>에러: {error}</div>;
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>식당 목록</h1>
      
      <div className={styles.searchContainer}>
        <input
          type="text"
          placeholder="식당 검색..."
          value={filter.search}
          onChange={handleSearch}
          className={styles.searchInput}
        />
      </div>

      <ul className={styles.restaurantList}>
        {restaurants.map((restaurant) => (
          <li key={restaurant.id} className={styles.restaurantItem}>
            {restaurant.name}
          </li>
        ))}
      </ul>
    </div>
  );
}
