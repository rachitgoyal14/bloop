export type Theme = 'dark' | 'light';

export interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

export interface FeatureCardProps {
  title: string;
  subtitle: string;
  features: string[];
  gridArea?: string;
}

export interface FAQItemProps {
  question: string;
  answer: string;
  isOpen: boolean;
  onClick: () => void;
}
