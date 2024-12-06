import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { assignmentAPI } from '@/api/assignment';

export const fetchAssignments = createAsyncThunk(
  'assignment/fetchAssignments',
  async (date) => {
    const response = await assignmentAPI.getAssignments(date);
    return response;
  }
);

export const createAssignment = createAsyncThunk(
  'assignment/createAssignment',
  async (date) => {
    const response = await assignmentAPI.createAssignment(date);
    return response;
  }
);

const initialState = {
  assignments: [],
  loading: false,
  error: null,
};

const assignmentSlice = createSlice({
  name: 'assignment',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAssignments.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchAssignments.fulfilled, (state, action) => {
        state.loading = false;
        state.assignments = action.payload;
        state.error = null;
      })
      .addCase(fetchAssignments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export default assignmentSlice.reducer; 