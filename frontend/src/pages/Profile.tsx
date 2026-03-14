import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '@/store';
import { updateTravelStyles, updateBudgetRange } from '@/store/slices/userSlice';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Slider } from '@/components/ui/slider';
import { motion } from 'framer-motion';

const travelStyleOptions = [
  '🏖️ Nghỉ dưỡng',
  '🗺️ Khám phá',
  '🎨 Văn hóa',
  '🍜 Ẩm thực',
  '🏃 Mạo hiểm',
  '🏛️ Lịch sử',
  '🛍️ Mua sắm',
  '🌅 Thiên nhiên',
];

const Profile = () => {
  const dispatch = useDispatch();
  const { preferences } = useSelector((state: RootState) => state.user);

  const toggleTravelStyle = (style: string) => {
    const newStyles = preferences.travelStyles.includes(style)
      ? preferences.travelStyles.filter((s) => s !== style)
      : [...preferences.travelStyles, style];
    dispatch(updateTravelStyles(newStyles));
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND',
    }).format(value);
  };

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        <div>
          <h1 className="text-3xl font-bold mb-2">Hồ sơ của tôi</h1>
          <p className="text-muted-foreground">
            Tùy chỉnh sở thích để nhận gợi ý phù hợp hơn
          </p>
        </div>

        {/* Travel Styles */}
        <Card>
          <CardHeader>
            <CardTitle>Phong cách du lịch</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-2">
              {travelStyleOptions.map((style) => (
                <Badge
                  key={style}
                  variant={
                    preferences.travelStyles.includes(style)
                      ? 'default'
                      : 'outline'
                  }
                  className={`cursor-pointer transition-all ${
                    preferences.travelStyles.includes(style)
                      ? 'gradient-ocean text-white'
                      : ''
                  }`}
                  onClick={() => toggleTravelStyle(style)}
                >
                  {style}
                </Badge>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Budget Range */}
        <Card>
          <CardHeader>
            <CardTitle>Ngân sách mặc định</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Slider
              value={preferences.budgetRange}
              onValueChange={(value) =>
                dispatch(updateBudgetRange(value as [number, number]))
              }
              min={0}
              max={50000000}
              step={500000}
              className="w-full"
            />
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground">
                {formatCurrency(preferences.budgetRange[0])}
              </span>
              <span className="text-muted-foreground">
                {formatCurrency(preferences.budgetRange[1])}
              </span>
            </div>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card className="border-primary/20 bg-primary/5">
          <CardContent className="pt-6">
            <p className="text-sm">
              💡 <strong>Mẹo:</strong> Cập nhật sở thích của bạn giúp trợ lý AI
              đưa ra những gợi ý phù hợp và cá nhân hóa hơn cho mọi chuyến đi!
            </p>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default Profile;
