---
name: mobile-typography
description: Mobile typography system for React Native and Flutter. Type scales, font weights, line heights, responsive typography, and dark mode support.
---

# Mobile Typography System

## Design Principles

Mobile typography requires special consideration due to:
- **Variable screen sizes** (375px - 428px+ width)
- **Viewing distance** (closer than desktop)
- **Touch interaction** (larger targets)
- **Outdoor usage** (higher contrast needed)

---

## React Native Type Scale

### Typography Configuration

```tsx
// typography.ts
export const typography = {
  // Font families
  fontFamily: {
    primary: 'System', // San Francisco (iOS) / Roboto (Android)
    secondary: 'System',
    monospace: 'Courier',
  },

  // Type scale (modular scale 1.25 for mobile)
  fontSize: {
    // Display & Headings
    displayLarge: 57,    // Hero titles
    displayMedium: 45,   // Page titles
    displaySmall: 36,    // Section headers

    // Headlines
    headlineLarge: 32,   // Featured content
    headlineMedium: 28,  // Cards headers
    headlineSmall: 24,   // List headers

    // Titles
    titleLarge: 22,      // Modal titles
    titleMedium: 16,     // List item titles
    titleSmall: 14,      // Subsection titles

    // Body
    bodyLarge: 16,       // Primary text
    bodyMedium: 14,      // Secondary text
    bodySmall: 12,       // Caption/helper

    // Labels
    labelLarge: 14,      // Buttons
    labelMedium: 12,     // Tabs
    labelSmall: 11,      // Badges
  },

  // Font weights
  fontWeight: {
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
  },

  // Line heights (optimal for mobile reading)
  lineHeight: {
    tight: 1.1,      // Display text
    snug: 1.25,      // Headings
    normal: 1.5,     // Body text
    relaxed: 1.75,   // Long-form content
  },

  // Letter spacing (in percentage)
  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
  },
};
```

### StyleSheet Helper

```tsx
// styles.ts
import { StyleSheet } from 'react-native';
import { typography } from './typography';

export const createTypographyStyles = () =>
  StyleSheet.create({
    // Display styles
    displayLarge: {
      fontSize: typography.fontSize.displayLarge,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 64,
      letterSpacing: -0.5,
    },
    displayMedium: {
      fontSize: typography.fontSize.displayMedium,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 52,
      letterSpacing: 0,
    },
    displaySmall: {
      fontSize: typography.fontSize.displaySmall,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 44,
      letterSpacing: 0,
    },

    // Headline styles
    headlineLarge: {
      fontSize: typography.fontSize.headlineLarge,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 40,
      letterSpacing: 0,
    },
    headlineMedium: {
      fontSize: typography.fontSize.headlineMedium,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 36,
      letterSpacing: 0,
    },
    headlineSmall: {
      fontSize: typography.fontSize.headlineSmall,
      fontWeight: typography.fontWeight.semibold,
      lineHeight: 32,
      letterSpacing: 0,
    },

    // Title styles
    titleLarge: {
      fontSize: typography.fontSize.titleLarge,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 28,
      letterSpacing: 0,
    },
    titleMedium: {
      fontSize: typography.fontSize.titleMedium,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 24,
      letterSpacing: 0.15,
    },
    titleSmall: {
      fontSize: typography.fontSize.titleSmall,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 20,
      letterSpacing: 0.1,
    },

    // Body styles
    bodyLarge: {
      fontSize: typography.fontSize.bodyLarge,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 24,
      letterSpacing: 0.5,
    },
    bodyMedium: {
      fontSize: typography.fontSize.bodyMedium,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 20,
      letterSpacing: 0.25,
    },
    bodySmall: {
      fontSize: typography.fontSize.bodySmall,
      fontWeight: typography.fontWeight.regular,
      lineHeight: 16,
      letterSpacing: 0.4,
    },

    // Label styles
    labelLarge: {
      fontSize: typography.fontSize.labelLarge,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 20,
      letterSpacing: 0.1,
    },
    labelMedium: {
      fontSize: typography.fontSize.labelMedium,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 16,
      letterSpacing: 0.5,
    },
    labelSmall: {
      fontSize: typography.fontSize.labelSmall,
      fontWeight: typography.fontWeight.medium,
      lineHeight: 16,
      letterSpacing: 0.5,
    },
  });
```

### Usage Examples

```tsx
// Components
import { createTypographyStyles } from './styles';

const styles = createTypographyStyles();

function ProfileHeader({ name, bio }: { name: string; bio: string }) {
  return (
    <View style={styles.container}>
      <Text style={styles.headlineMedium}>{name}</Text>
      <Text style={styles.bodyMedium}>{bio}</Text>
    </View>
  );
}

function Button({ label }: { label: string }) {
  return (
    <TouchableOpacity style={buttonStyles.button}>
      <Text style={styles.labelLarge}>{label}</Text>
    </TouchableOpacity>
  );
}

function Card({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <View style={cardStyles.card}>
      <Text style={styles.titleMedium}>{title}</Text>
      <Text style={styles.bodySmall}>{subtitle}</Text>
    </View>
  );
}
```

---

## Flutter Type Scale

### Typography Configuration

```dart
// typography.dart
import 'package:flutter/material.dart';

class AppTypography {
  // Font families
  static const String fontFamilyPrimary = 'System';
  static const String fontFamilySecondary = 'System';

  // Text styles
  static const TextStyle displayLarge = TextStyle(
    fontSize: 57,
    fontWeight: FontWeight.w400,
    letterSpacing: -0.25,
    height: 1.12, // 64px line height
  );

  static const TextStyle displayMedium = TextStyle(
    fontSize: 45,
    fontWeight: FontWeight.w400,
    height: 1.16, // 52px line height
  );

  static const TextStyle displaySmall = TextStyle(
    fontSize: 36,
    fontWeight: FontWeight.w400,
    height: 1.22, // 44px line height
  );

  static const TextStyle headlineLarge = TextStyle(
    fontSize: 32,
    fontWeight: FontWeight.w400,
    height: 1.25, // 40px line height
  );

  static const TextStyle headlineMedium = TextStyle(
    fontSize: 28,
    fontWeight: FontWeight.w400,
    height: 1.29, // 36px line height
  );

  static const TextStyle headlineSmall = TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.w600,
    height: 1.33, // 32px line height
  );

  static const TextStyle titleLarge = TextStyle(
    fontSize: 22,
    fontWeight: FontWeight.w500,
    height: 1.27, // 28px line height
  );

  static const TextStyle titleMedium = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w500,
    height: 1.5, // 24px line height
    letterSpacing: 0.15,
  );

  static const TextStyle titleSmall = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    height: 1.43, // 20px line height
    letterSpacing: 0.1,
  );

  static const TextStyle bodyLarge = TextStyle(
    fontSize: 16,
    fontWeight: FontWeight.w400,
    height: 1.5, // 24px line height
    letterSpacing: 0.5,
  );

  static const TextStyle bodyMedium = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w400,
    height: 1.43, // 20px line height
    letterSpacing: 0.25,
  );

  static const TextStyle bodySmall = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w400,
    height: 1.33, // 16px line height
    letterSpacing: 0.4,
  );

  static const TextStyle labelLarge = TextStyle(
    fontSize: 14,
    fontWeight: FontWeight.w500,
    height: 1.43, // 20px line height
    letterSpacing: 0.1,
  );

  static const TextStyle labelMedium = TextStyle(
    fontSize: 12,
    fontWeight: FontWeight.w500,
    height: 1.33, // 16px line height
    letterSpacing: 0.5,
  );

  static const TextStyle labelSmall = TextStyle(
    fontSize: 11,
    fontWeight: FontWeight.w500,
    height: 1.45, // 16px line height
    letterSpacing: 0.5,
  );
}

// Material 3 Theme with typography
ThemeData buildTheme() {
  return ThemeData(
    textTheme: TextTheme(
      displayLarge: AppTypography.displayLarge,
      displayMedium: AppTypography.displayMedium,
      displaySmall: AppTypography.displaySmall,
      headlineLarge: AppTypography.headlineLarge,
      headlineMedium: AppTypography.headlineMedium,
      headlineSmall: AppTypography.headlineSmall,
      titleLarge: AppTypography.titleLarge,
      titleMedium: AppTypography.titleMedium,
      titleSmall: AppTypography.titleSmall,
      bodyLarge: AppTypography.bodyLarge,
      bodyMedium: AppTypography.bodyMedium,
      bodySmall: AppTypography.bodySmall,
      labelLarge: AppTypography.labelLarge,
      labelMedium: AppTypography.labelMedium,
      labelSmall: AppTypography.labelSmall,
    ),
  );
}
```

### Usage Examples

```dart
// Widgets
class ProfileHeader extends StatelessWidget {
  final String name;
  final String bio;

  const ProfileHeader({required this.name, required this.bio});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(name, style: Theme.of(context).textTheme.displayMedium),
        SizedBox(height: 8),
        Text(bio, style: Theme.of(context).textTheme.bodyMedium),
      ],
    );
  }
}

class StyledButton extends StatelessWidget {
  final String label;

  const StyledButton({required this.label});

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {},
      child: Text(
        label,
        style: Theme.of(context).textTheme.labelLarge,
      ),
    );
  }
}
```

---

## Responsive Typography

### React Native

```tsx
import { Dimensions, StyleSheet } from 'react-native';

const { width } = Dimensions.get('window');

// Base dimensions for scaling
const baseWidth = 390; // iPhone 14

// Scale factor helper
const scale = (size: number) => {
  return Math.round((size * width) / baseWidth);
};

export const responsiveTypography = StyleSheet.create({
  // Scales proportionally with screen width
  displayLarge: {
    fontSize: scale(57),
    fontWeight: '400',
    lineHeight: scale(64),
  },
  headlineMedium: {
    fontSize: scale(28),
    fontWeight: '400',
    lineHeight: scale(36),
  },
  bodyMedium: {
    fontSize: scale(14),
    fontWeight: '400',
    lineHeight: scale(20),
  },
});
```

### Flutter

```dart
class ResponsiveText extends StatelessWidget {
  final String text;
  final TextStyle style;

  const ResponsiveText({
    required this.text,
    required this.style,
  });

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final scaleFactor = screenWidth / 390; // Base width

    return Text(
      text,
      style: style.copyWith(
        fontSize: style.fontSize! * scaleFactor.clamp(0.85, 1.15),
      ),
    );
  }
}
```

---

## Dark Mode Typography

### React Native

```tsx
// Dark mode color adjustments for typography
export const darkThemeColors = {
  text: {
    // High contrast for dark backgrounds
    primary: '#FFFFFF',      // 100% opacity
    secondary: '#E3E3E3',    // 87% opacity
    tertiary: '#A0A0A0',     // 60% opacity
    disabled: '#4F4F4F',     // 38% opacity
  },
  background: {
    primary: '#121212',
    secondary: '#1E1E1E',
  },
};

// Apply to styles
const darkStyles = StyleSheet.create({
  headlineMedium: {
    fontSize: 28,
    fontWeight: '400',
    color: darkThemeColors.text.primary,
  },
  bodyMedium: {
    fontSize: 14,
    fontWeight: '400',
    color: darkThemeColors.text.secondary,
  },
  caption: {
    fontSize: 12,
    fontWeight: '400',
    color: darkThemeColors.text.tertiary,
  },
});
```

### Flutter

```dart
class DarkThemeColors {
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFE3E3E3);
  static const Color textTertiary = Color(0xFFA0A0A0);
  static const Color textDisabled = Color(0xFF4F4F4F);

  static ThemeData buildDarkTheme() {
    return ThemeData(
      brightness: Brightness.dark,
      textTheme: TextTheme(
        displayMedium: AppTypography.displayMedium.copyWith(
          color: textPrimary,
        ),
        bodyMedium: AppTypography.bodyMedium.copyWith(
          color: textSecondary,
        ),
        bodySmall: AppTypography.bodySmall.copyWith(
          color: textTertiary,
        ),
      ),
    );
  }
}
```

---

## Best Practices

### DO's

```tsx
// ✅ Use appropriate text style hierarchy
<Text style={styles.headlineMedium}>Page Title</Text>
<Text style={styles.bodyMedium}>Description</Text>

// ✅ Maintain consistent line height for readability
<Text style={[styles.bodyLarge, { lineHeight: 24 }]}>
  Long-form content with proper spacing
</Text>

// ✅ Use medium/semibold for emphasis (not bold)
<Text style={[styles.titleMedium, { fontWeight: '600' }]}>
  Important Information
</Text>

// ✅ Respect minimum readable size (12px)
<Text style={styles.bodySmall}>Caption text</Text>
```

### DON'Ts

```tsx
// ❌ Don't use arbitrary font sizes
<Text style={{ fontSize: 23 }}>Wrong</Text>

// ❌ Don't use bold for body text
<Text style={{ fontWeight: '700' }}>Hard to read</Text>

// ❌ Don't use font size below 11px
<Text style={{ fontSize: 10 }}>Too small</Text>

// ❌ Don't ignore line height
<Text style={{ lineHeight: 1 }}>Cramped text</Text>
```

---

## Type Scale Reference

| Style | React Native | Flutter | Usage |
|-------|--------------|---------|-------|
| **Display** |
| displayLarge | 57px | 57px | Hero titles |
| displayMedium | 45px | 45px | Page titles |
| displaySmall | 36px | 36px | Section headers |
| **Headline** |
| headlineLarge | 32px | 32px | Featured content |
| headlineMedium | 28px | 28px | Card headers |
| headlineSmall | 24px | 24px | List headers |
| **Title** |
| titleLarge | 22px | 22px | Modal titles |
| titleMedium | 16px | 16px | List items |
| titleSmall | 14px | 14px | Subsections |
| **Body** |
| bodyLarge | 16px | 16px | Primary text |
| bodyMedium | 14px | 14px | Secondary text |
| bodySmall | 12px | 12px | Captions |
| **Label** |
| labelLarge | 14px | 14px | Buttons |
| labelMedium | 12px | 12px | Tabs |
| labelSmall | 11px | 11px | Badges |

---

## Font Weight Reference

| Name | Value | Usage |
|------|-------|-------|
| Regular | 400 | Body text, display |
| Medium | 500 | Emphasis, buttons |
| Semibold | 600 | Headings, titles |
| Bold | 700 | Strong emphasis (rare) |

---

## Line Height Reference

| Name | Ratio | Usage |
|------|-------|-------|
| Tight | 1.1 | Display text |
| Snug | 1.25 | Headings |
| Normal | 1.5 | Body text (recommended) |
| Relaxed | 1.75 | Long-form content |
