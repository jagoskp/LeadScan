import React, { useState } from 'react';
import { TaskBoard } from '../components/TaskBoard';
import { useTasks } from '../hooks/useTasks';

export const WorkflowAutomationPage: React.FC = () => {
  const { tasks, loading, addTask, markComplete } = useTasks();
  const [newTitle, setNewTitle] = useState<string>('');
  const [priority, setPriority] = useState<string>('Medium');

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim()) return;
    addTask(newTitle, priority);
    setNewTitle('');
  };

  return (
    <div
      style={{
        padding: '32px',
        background: '#0f1117',
        minHeight: '100vh',
        color: '#fff',
        fontFamily: 'Inter, system-ui, sans-serif',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ margin: 0, fontSize: '1.8rem', fontWeight: 800 }}>Enterprise Workflow & Automation Engine</h1>
          <p style={{ color: '#9ca3af', fontSize: '0.95rem', marginTop: '4px' }}>
            Task management, follow-up scheduling, reminder engine, SLA tracking, and automated rule execution.
          </p>
        </div>
      </div>

      <form
        onSubmit={handleCreate}
        style={{
          background: '#1a1d24',
          padding: '16px',
          borderRadius: '8px',
          border: '1px solid #374151',
          display: 'flex',
          gap: '12px',
          marginBottom: '24px',
        }}
      >
        <input
          type="text"
          placeholder="New Task Title (e.g. Schedule Product Demo)"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          style={{ flex: 1, background: '#111827', border: '1px solid #374151', borderRadius: '6px', color: '#fff', padding: '10px' }}
        />
        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          style={{ background: '#111827', border: '1px solid #374151', borderRadius: '6px', color: '#fff', padding: '10px' }}
        >
          <option value="High">High Priority</option>
          <option value="Medium">Medium Priority</option>
          <option value="Low">Low Priority</option>
        </select>
        <button
          type="submit"
          style={{ background: '#3B82F6', color: '#fff', border: 'none', borderRadius: '6px', padding: '10px 20px', fontWeight: 700, cursor: 'pointer' }}
        >
          + Add Task
        </button>
      </form>

      <TaskBoard tasks={tasks} onComplete={markComplete} loading={loading} />
    </div>
  );
};

export default WorkflowAutomationPage;
