import React from 'react';
import { Task } from '../types/workflow';
import { getPriorityBadgeColor } from '../utils/workflowUtils';

interface Props {
  tasks: Task[];
  onComplete: (taskId: string) => void;
  loading: boolean;
}

export const TaskBoard: React.FC<Props> = ({ tasks, onComplete, loading }) => {
  if (loading) return <p style={{ color: '#9ca3af' }}>Loading workflow tasks...</p>;
  if (tasks.length === 0) return <p style={{ color: '#9ca3af' }}>No active workflow tasks.</p>;

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
      {tasks.map((task) => {
        const badgeColor = getPriorityBadgeColor(task.priority);
        return (
          <div
            key={task.id}
            style={{
              background: '#1a1d24',
              border: '1px solid #374151',
              borderRadius: '8px',
              padding: '16px',
              color: '#fff',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
            }}
          >
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                <span
                  style={{
                    background: `${badgeColor}20`,
                    color: badgeColor,
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: '4px',
                  }}
                >
                  {task.priority} Priority
                </span>
                <span style={{ fontSize: '0.75rem', color: task.status === 'Completed' ? '#10B981' : '#F59E0B' }}>
                  {task.status}
                </span>
              </div>
              <h4 style={{ margin: '0 0 6px 0', fontSize: '1rem' }}>{task.title}</h4>
              {task.description && <p style={{ fontSize: '0.85rem', color: '#9ca3af', margin: 0 }}>{task.description}</p>}
            </div>

            {task.status !== 'Completed' && (
              <button
                onClick={() => onComplete(task.id)}
                style={{
                  marginTop: '16px',
                  background: '#10B981',
                  color: '#fff',
                  border: 'none',
                  borderRadius: '4px',
                  padding: '6px 12px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                ✓ Complete Task
              </button>
            )}
          </div>
        );
      })}
    </div>
  );
};
