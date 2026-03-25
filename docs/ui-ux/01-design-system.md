# Design System

## Color Tokens

All colors use CSS custom properties for easy theme switching.

### Playful Theme - Light

```css
--color-bg-primary: #F8FAFB;
--color-bg-card: #FFFFFF;
--color-bg-accent: linear-gradient(135deg, #E0F7FA, #F0F4FF);

--color-text-primary: #1A2B3C;
--color-text-secondary: #5A6B7C;
--color-text-muted: #8A9BAC;

--color-brand-primary: #26A69A;      /* soft teal */
--color-brand-secondary: #FF8A65;    /* warm coral accent */

--color-status-safe: #43A047;
--color-status-attention: #FB8C00;
--color-status-risk: #E53935;

--color-border: #E0E6ED;
--color-shadow: rgba(0, 0, 0, 0.08);
```

### Playful Theme - Dark

```css
--color-bg-primary: #1A1E2E;
--color-bg-card: #242838;
--color-bg-accent: linear-gradient(135deg, #1A2E2C, #1E2440);

--color-text-primary: #E8ECF0;
--color-text-secondary: #A0AABB;
--color-text-muted: #6A7A8B;

--color-brand-primary: #4DB6AC;      /* slightly desaturated teal */
--color-brand-secondary: #FFAB91;    /* softened coral */

--color-status-safe: #66BB6A;
--color-status-attention: #FFA726;
--color-status-risk: #EF5350;

--color-border: #2E3448;
--color-shadow: rgba(0, 0, 0, 0.3);
```

### Minimal Theme - Light

```css
--color-bg-primary: #FAFAFA;
--color-bg-card: #FFFFFF;
--color-bg-accent: #F5F5F5;

--color-brand-primary: #546E7A;      /* muted blue-grey */
--color-brand-secondary: #78909C;

/* Status and text colors same as Playful Light */
```

### Minimal Theme - Dark

```css
--color-bg-primary: #1C1C1E;
--color-bg-card: #2C2C2E;
--color-bg-accent: #242426;

--color-brand-primary: #78909C;
--color-brand-secondary: #90A4AE;

/* Status and text colors same as Playful Dark */
```

## Typography

```css
--font-family: 'Inter', system-ui, sans-serif;

--font-size-xs: 0.75rem;    /* 12px */
--font-size-sm: 0.875rem;   /* 14px */
--font-size-base: 1rem;     /* 16px */
--font-size-lg: 1.125rem;   /* 18px */
--font-size-xl: 1.5rem;     /* 24px */
--font-size-2xl: 2rem;      /* 32px */

--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

## Spacing

```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-5: 1.5rem;    /* 24px */
--space-6: 2rem;      /* 32px */
--space-8: 3rem;      /* 48px */
```

## Border Radius

```css
/* Playful theme */
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
--radius-full: 9999px;

/* Minimal theme */
--radius-sm: 4px;
--radius-md: 6px;
--radius-lg: 8px;
--radius-full: 9999px;
```

## Shadows

```css
/* Playful theme */
--shadow-sm: 0 1px 3px var(--color-shadow);
--shadow-md: 0 4px 12px var(--color-shadow);
--shadow-lg: 0 8px 24px var(--color-shadow);

/* Minimal theme - subtler shadows */
--shadow-sm: 0 1px 2px var(--color-shadow);
--shadow-md: 0 2px 8px var(--color-shadow);
--shadow-lg: 0 4px 16px var(--color-shadow);
```

## Breakpoints

| Name | Width | Usage |
|------|-------|-------|
| `sm` | 640px | Mobile landscape |
| `md` | 768px | Tablet |
| `lg` | 1024px | Desktop (sidebar visible) |
| `xl` | 1280px | Wide desktop |
