// Mock API client to replace Base44
const createMockEntity = (entityName) => {
  const storageKey = `${entityName.toLowerCase()}_data`;
  
  return {
    list: async (sortField) => {
      const data = JSON.parse(localStorage.getItem(storageKey) || '[]');
      return data;
    },
    
    filter: async (conditions, sortField) => {
      const data = JSON.parse(localStorage.getItem(storageKey) || '[]');
      return data.filter(item => {
        return Object.entries(conditions).every(([key, value]) => item[key] === value);
      });
    },
    
    create: async (newData) => {
      const data = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const item = { ...newData, id: Date.now().toString() };
      data.push(item);
      localStorage.setItem(storageKey, JSON.stringify(data));
      return item;
    },
    
    update: async (id, updates) => {
      const data = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const index = data.findIndex(item => item.id === id);
      if (index !== -1) {
        data[index] = { ...data[index], ...updates };
        localStorage.setItem(storageKey, JSON.stringify(data));
      }
      return data[index];
    },
    
    delete: async (id) => {
      const data = JSON.parse(localStorage.getItem(storageKey) || '[]');
      const filtered = data.filter(item => item.id !== id);
      localStorage.setItem(storageKey, JSON.stringify(filtered));
      return { success: true };
    }
  };
};

export const base44 = {
  entities: {
    Position: createMockEntity('Position'),
    Portfolio: createMockEntity('Portfolio'),
    Settings: createMockEntity('Settings'),
    MarketRegime: createMockEntity('MarketRegime'),
  }
};
