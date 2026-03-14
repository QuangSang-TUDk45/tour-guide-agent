import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { Calendar, MapPin, Trash2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';

const Trips = () => {
  const { savedTrips } = useSelector((state: RootState) => state.trip);

  return (
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold mb-2">Lịch sử chuyến đi</h1>
        <p className="text-muted-foreground mb-8">
          Xem lại các kế hoạch du lịch bạn đã lưu
        </p>

        {savedTrips.length === 0 ? (
          <Card className="text-center py-12">
            <CardContent>
              <div className="w-16 h-16 mx-auto mb-4 rounded-full gradient-ocean flex items-center justify-center">
                <Calendar className="h-8 w-8 text-white" />
              </div>
              <h3 className="text-lg font-semibold mb-2">
                Chưa có chuyến đi nào
              </h3>
              <p className="text-muted-foreground mb-4">
                Bắt đầu lên kế hoạch cho chuyến đi đầu tiên của bạn!
              </p>
              <Button className="gradient-ocean">Bắt đầu lập kế hoạch</Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {savedTrips.map((trip) => (
              <motion.div
                key={trip.id}
                whileHover={{ scale: 1.02 }}
                className="h-full"
              >
                <Card className="h-full shadow-card hover:shadow-card-hover transition-all">
                  <CardHeader>
                    <CardTitle className="flex items-start justify-between">
                      <span>{trip.title}</span>
                      <Button variant="ghost" size="icon" className="h-8 w-8">
                        <Trash2 className="h-4 w-4 text-destructive" />
                      </Button>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <MapPin className="h-4 w-4" />
                      <span>{trip.destination}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-muted-foreground">
                      <Calendar className="h-4 w-4" />
                      <span>
                        {trip.startDate} - {trip.endDate}
                      </span>
                    </div>
                    <Button className="w-full gradient-ocean">
                      Xem chi tiết
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default Trips;
