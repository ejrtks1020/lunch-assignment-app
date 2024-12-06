'use client';

import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchAssignments, createAssignment } from '@/store/slices/assignmentSlice';
import styles from './page.module.css';

export default function Home() {
  const dispatch = useDispatch();
  const { assignments, loading, error } = useSelector((state) => state.assignment);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    if (selectedDate) {
      dispatch(fetchAssignments(selectedDate));
    }
  }, [selectedDate, dispatch]);

  const handleCreateAssignment = async () => {
    try {
      await dispatch(createAssignment(selectedDate)).unwrap();
      dispatch(fetchAssignments(selectedDate));
    } catch (error) {
      console.error('배정 생성 실패:', error);
    }
  };

  const groupedAssignments = assignments.reduce((groups, assignment) => {
    const restaurantId = assignment.restaurant_id;
    if (!groups[restaurantId]) {
      groups[restaurantId] = {
        restaurant_id: restaurantId,
        restaurant_name: assignment.restaurant_name || `식당 ${restaurantId}`,
        users: [],
        assignment_date: assignment.assignment_date
      };
    }
    groups[restaurantId].users.push(assignment.user_name || `사용자 ${assignment.user_id}`);
    return groups;
  }, {});

  if (loading) {
    return <div className={styles.loading}>로딩 중...</div>;
  }

  if (error) {
    return <div className={styles.error}>에러: {error}</div>;
  }

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <h1 className={styles.title}>오늘의 점심 그룹</h1>
        
        <div className={styles.dateContainer}>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className={styles.dateInput}
          />
          <button 
            onClick={handleCreateAssignment}
            className={styles.createButton}
          >
            새로운 그룹 생성
          </button>
        </div>

        <div className={styles.assignmentList}>
          {Object.values(groupedAssignments).map((group, index) => (
            <div key={group.restaurant_id} className={styles.assignmentItem}>
              <h3>{group.restaurant_name}</h3>
              <div className={styles.memberList}>
                <h4>멤버</h4>
                <ul>
                  {group.users.map((user, userIndex) => (
                    <li key={userIndex}>{user}</li>
                  ))}
                </ul>
              </div>
              <p className={styles.date}>날짜: {group.assignment_date}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
