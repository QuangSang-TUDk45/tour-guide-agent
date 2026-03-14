import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Trip {
  id: string;
  title: string;
  destination: string;
  startDate: string;
  endDate: string;
  itinerary: any[];
  createdAt: Date;
}

interface TripState {
  savedTrips: Trip[];
  currentTrip: Trip | null;
}

const initialState: TripState = {
  savedTrips: [],
  currentTrip: null,
};

const tripSlice = createSlice({
  name: 'trip',
  initialState,
  reducers: {
    saveTrip: (state, action: PayloadAction<Trip>) => {
      state.savedTrips.push(action.payload);
    },
    setCurrentTrip: (state, action: PayloadAction<Trip | null>) => {
      state.currentTrip = action.payload;
    },
    deleteTrip: (state, action: PayloadAction<string>) => {
      state.savedTrips = state.savedTrips.filter(trip => trip.id !== action.payload);
    },
  },
});

export const { saveTrip, setCurrentTrip, deleteTrip } = tripSlice.actions;
export default tripSlice.reducer;
