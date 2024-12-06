import apiClient from '@/lib/axios';

export const assignmentAPI = {
  getAssignments: async (date) => {
    const response = await apiClient.get(`/restaurant/assignments/${date}`);
    return response.data;
  },
  
  createAssignment: async (date) => {
    const response = await apiClient.post('/restaurant/assign', { assignment_date: date });
    return response.data;
  }
}; 