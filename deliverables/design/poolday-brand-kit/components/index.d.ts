import type * as React from 'react';
export type IconName = 'layout-grid' | 'briefcase' | 'gamepad-2' | 'mic' | 'chevron-down' | 'volume-2';
export interface IconProps { name: IconName; size?: number; className?: string }
export declare function Icon(props: IconProps): React.ReactElement;
export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { size?: 'md' | 'lg'; href?: string; icon?: IconName }
/** The off-white pill. md = 40px (nav), lg = 50px (hero). */
export declare function Button(props: ButtonProps): React.ReactElement;
export interface NavLink { label: string; href?: string; menu?: boolean }
export interface NavBarProps { links?: NavLink[]; cta?: string; ctaHref?: string; homeHref?: string; className?: string }
export declare function NavBar(props: NavBarProps): React.ReactElement;
export interface TabItem { id: string; label: string; icon?: IconName }
export interface FilterTabsProps { items?: TabItem[]; value?: string; defaultValue?: string; onChange?: (id: string) => void; className?: string }
export declare function FilterTabs(props: FilterTabsProps): React.ReactElement;
export interface VideoCardProps { src?: string; poster?: string; title?: string; tag?: string; recipe?: string; span?: 1 | 2; sound?: boolean; tint?: string; className?: string }
export declare function VideoCard(props: VideoCardProps): React.ReactElement;
export declare function VideoGrid(props: { children?: React.ReactNode; className?: string }): React.ReactElement;
export interface SectionTitleProps { lead: React.ReactNode; tail?: React.ReactNode; as?: 'h1' | 'h2' | 'h3'; className?: string }
export declare function SectionTitle(props: SectionTitleProps): React.ReactElement;
export interface HalftoneProps { centerX?: number; centerY?: number; radiusX?: number; radiusY?: number; animate?: boolean; className?: string }
export declare function Halftone(props: HalftoneProps): React.ReactElement;
export interface HeroProps { title?: React.ReactNode; lede?: React.ReactNode; cta?: string; ctaHref?: string; animate?: boolean; className?: string }
export declare function Hero(props: HeroProps): React.ReactElement;
declare global { interface Window { Poolday: { Icon: typeof Icon; Button: typeof Button; NavBar: typeof NavBar; FilterTabs: typeof FilterTabs; VideoCard: typeof VideoCard; VideoGrid: typeof VideoGrid; SectionTitle: typeof SectionTitle; Halftone: typeof Halftone; Hero: typeof Hero } } }
