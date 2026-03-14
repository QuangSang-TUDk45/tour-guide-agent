import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface UserPreferences {
  travelStyles: string[];
  budgetRange: [number, number];
  favoriteDestinations: string[];
}

interface UserState {
  preferences: UserPreferences;
  isAuthenticated: boolean;
}

const initialState: UserState = {
  preferences: {
    travelStyles: [],
    budgetRange: [0, 10000000],
    favoriteDestinations: [],
  },
  isAuthenticated: false,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setPreferences: (state, action: PayloadAction<UserPreferences>) => {
      state.preferences = action.payload;
    },
    updateTravelStyles: (state, action: PayloadAction<string[]>) => {
      state.preferences.travelStyles = action.payload;
    },
    updateBudgetRange: (state, action: PayloadAction<[number, number]>) => {
      state.preferences.budgetRange = action.payload;
    },
    setAuthenticated: (state, action: PayloadAction<boolean>) => {
      state.isAuthenticated = action.payload;
    },
  },
});

export const { setPreferences, updateTravelStyles, updateBudgetRange, setAuthenticated } = userSlice.actions;
export default userSlice.reducer;
