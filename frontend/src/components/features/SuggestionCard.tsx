import { motion } from 'framer-motion';
import { Star, MapPin, DollarSign, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

interface SuggestionCardProps {
  suggestion: {
    id: string;
    name: string;
    image: string;
    rating: number;
    priceRange: string;
    location: string;
    tags: string[];
  };
}

const SuggestionCard = ({ suggestion }: SuggestionCardProps) => {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      className="bg-background rounded-xl overflow-hidden border shadow-card hover:shadow-card-hover transition-all"
    >
      {/* Image */}
      <div className="relative h-48 overflow-hidden">
        <img
          src={suggestion.image}
          alt={suggestion.name}
          className="w-full h-full object-cover"
        />
        <button className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm rounded-full p-2 hover:bg-white transition-colors">
          <Heart className="h-4 w-4 text-destructive" />
        </button>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        <div>
          <h3 className="font-semibold text-lg mb-1">{suggestion.name}</h3>
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Star className="h-4 w-4 fill-yellow-400 text-yellow-400" />
              <span>{suggestion.rating}</span>
            </div>
            <div className="flex items-center gap-1">
              <MapPin className="h-4 w-4" />
              <span>{suggestion.location}</span>
            </div>
            <div className="flex items-center gap-1">
              <DollarSign className="h-4 w-4" />
              <span>{suggestion.priceRange}</span>
            </div>
          </div>
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-2">
          {suggestion.tags.map((tag, idx) => (
            <Badge key={idx} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
        </div>

        {/* Actions */}
        <div className="flex gap-2 pt-2">
          <Button className="flex-1 gradient-ocean" size="sm">
            Chọn
          </Button>
          <Button variant="outline" size="sm">
            Chi tiết
          </Button>
        </div>
      </div>
    </motion.div>
  );
};

export default SuggestionCard;
