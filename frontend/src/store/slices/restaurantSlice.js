
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { restaurantAPI } from '@/api/restaurant';

export const fetchRestaurants = createAsyncThunk(
  'restaurant/fetchRestaurants',
  async () => {
    const response = await restaurantAPI.getRestaurants();
    return response;
  }
);

export const searchRestaurants = createAsyncThunk(
  'restaurant/searchRestaurants',
  async (query) => {
    const response = await restaurantAPI.searchRestaurants(query);
    return response;
  }
);

export const getRestaurantById = createAsyncThunk(
  'restaurant/getRestaurantById',
  async (id) => {
    const response = await restaurantAPI.getRestaurantById(id);
    return response;
  }
);

const initialState = {
  restaurants: [],
  selectedRestaurant: null,
  loading: false,
  error: null,
  filter: {
    search: '',
    tags: [],
    rating: 0,
  },
};

const restaurantSlice = createSlice({
  name: 'restaurant',
  initialState,
  reducers: {
    setFilter: (state, action) => {
      state.filter = { ...state.filter, ...action.payload };
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchRestaurants.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchRestaurants.fulfilled, (state, action) => {
        state.loading = false;
        state.restaurants = action.payload;
        state.error = null;
      })
      .addCase(fetchRestaurants.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(searchRestaurants.pending, (state) => {
        state.loading = true;
      })
      .addCase(searchRestaurants.fulfilled, (state, action) => {
        state.loading = false;
        state.restaurants = action.payload;
        state.error = null;
      })
      .addCase(getRestaurantById.fulfilled, (state, action) => {
        state.selectedRestaurant = action.payload;
      });
  },
});

export const { setFilter } = restaurantSlice.actions;
export default restaurantSlice.reducer; 