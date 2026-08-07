import { useCallback, useEffect, useState } from 'react';
import { workflowApi } from '../services/workflowApi';
import { Task } from '../types/workflow';

export function useTasks(leadId?: string, initialStatus?: string) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    try {
      const data = await workflowApi.listTasks(leadId, initialStatus);
      setTasks(data);
    } catch (e) {
      console.error('Failed to load tasks', e);
    } finally {
      setLoading(false);
    }
  }, [leadId, initialStatus]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const addTask = async (title: string, priority: string = 'Medium') => {
    try {
      const newTask = await workflowApi.createTask(title, leadId, priority);
      setTasks((prev) => [newTask, ...prev]);
    } catch (e) {
      console.error('Failed to add task', e);
    }
  };

  const markComplete = async (taskId: string) => {
    try {
      const updated = await workflowApi.completeTask(taskId);
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
    } catch (e) {
      console.error('Failed to complete task', e);
    }
  };

  return { tasks, loading, addTask, markComplete, refetchTasks: fetchTasks };
}
