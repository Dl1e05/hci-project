import type { ContentBannerProps } from "@/app/(pages)/home/components/Content-banner";



// A1 Level
export const fallbackA1Content: ContentBannerProps[] = [
    {
        id: 'a1-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/0891b2/ffffff?text=Finding+Nemo',
        href: '/content/a1/movies'
    },
    {
        id: 'a1-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/8b5cf6/ffffff?text=Peppa+Pig',
        href: '/content/a1/tv-shows'
    },
    {
        id: 'a1-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/dc2626/ffffff?text=Wimpy+Kid',
        href: '/content/a1/books'
    },
    {
        id: 'a1-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/64748b/ffffff?text=Minecraft',
        href: '/content/a1/games'
    }
];

// A2 Level
export const fallbackA2Content: ContentBannerProps[] = [
    {
        id: 'a2-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/0c4a6e/ffffff?text=Paddington',
        href: '/content/a2/movies'
    },
    {
        id: 'a2-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/059669/ffffff?text=SpongeBob',
        href: '/content/a2/tv-shows'
    },
    {
        id: 'a2-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/7c2d12/ffffff?text=Roald+Dahl',
        href: '/content/a2/books'
    },
    {
        id: 'a2-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/16a34a/ffffff?text=Animal+Crossing',
        href: '/content/a2/games'
    }
];

// B1 Level
export const fallbackB1Content: ContentBannerProps[] = [
    {
        id: 'b1-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/1e293b/ffffff?text=Harry+Potter',
        href: '/content/b1/movies'
    },
    {
        id: 'b1-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/9333ea/ffffff?text=Gilmore+Girls',
        href: '/content/b1/tv-shows'
    },
    {
        id: 'b1-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/ca8a04/ffffff?text=Wizard+of+Oz',
        href: '/content/b1/books'
    },
    {
        id: 'b1-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/78716c/ffffff?text=Life+is+Strange',
        href: '/content/b1/games'
    }
];

// B2 Level
export const fallbackB2Content: ContentBannerProps[] = [
    {
        id: 'b2-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/1e40af/ffffff?text=The+Social+Network',
        href: '/content/b2/movies'
    },
    {
        id: 'b2-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/be123c/ffffff?text=Breaking+Bad',
        href: '/content/b2/tv-shows'
    },
    {
        id: 'b2-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/0f766e/ffffff?text=1984',
        href: '/content/b2/books'
    },
    {
        id: 'b2-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/4338ca/ffffff?text=The+Last+of+Us',
        href: '/content/b2/games'
    }
];

// C1 Level
export const fallbackC1Content: ContentBannerProps[] = [
    {
        id: 'c1-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/0f172a/ffffff?text=Inception',
        href: '/content/c1/movies'
    },
    {
        id: 'c1-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/881337/ffffff?text=The+Crown',
        href: '/content/c1/tv-shows'
    },
    {
        id: 'c1-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/713f12/ffffff?text=Crime+and+Punishment',
        href: '/content/c1/books'
    },
    {
        id: 'c1-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/065f46/ffffff?text=Red+Dead+Redemption',
        href: '/content/c1/games'
    }
];

// C2 Level
export const fallbackC2Content: ContentBannerProps[] = [
    {
        id: 'c2-1',
        title: 'Movies',
        imageUrl: 'https://placehold.co/400x600/18181b/ffffff?text=The+Godfather',
        href: '/content/c2/movies'
    },
    {
        id: 'c2-2',
        title: 'TV shows',
        imageUrl: 'https://placehold.co/400x600/7c2d12/ffffff?text=Mad+Men',
        href: '/content/c2/tv-shows'
    },
    {
        id: 'c2-3',
        title: 'Books',
        imageUrl: 'https://placehold.co/400x600/14532d/ffffff?text=Ulysses',
        href: '/content/c2/books'
    },
    {
        id: 'c2-4',
        title: 'Games',
        imageUrl: 'https://placehold.co/400x600/312e81/ffffff?text=Disco+Elysium',
        href: '/content/c2/games'
    }
];

// Типы для уровней
export type LanguageLevel = {
    level: string;
    description: string;
    badge: string;
    content: ContentBannerProps[];
};

// Все уровни в одном объекте
export const languageLevels: Record<string, LanguageLevel> = {
    A1: {
        level: "A1 Level",
        description: "A1 is the beginner level, where learners start with simple words, phrases, and everyday expressions. At this stage, students can introduce themselves, ask basic questions, and understand short, clear communication.",
        badge: "Beginner",
        content: fallbackA1Content
    },
    A2: {
        level: "A2 Level",
        description: "A2 is the elementary level, where learners can understand and use basic English for everyday situations. At this stage, they can communicate in simple tasks, describe their routine, and understand short, clear texts and conversations.",
        badge: "Elementary",
        content: fallbackA2Content
    },
    B1: {
        level: "B1 Level",
        description: "B1 is the intermediate level, where learners can communicate in everyday situations using more complex sentences and vocabulary. They can describe experiences, express opinions, and understand the main points of texts and conversations.",
        badge: "Intermediate",
        content: fallbackB1Content
    },
    B2: {
        level: "B2 Level",
        description: "B2 is the upper-intermediate level, where learners can interact with a degree of fluency and spontaneity. They can produce detailed text on various subjects and understand complex texts on both concrete and abstract topics.",
        badge: "Upper-Intermediate",
        content: fallbackB2Content
    },
    C1: {
        level: "C1 Level",
        description: "C1 is the advanced level, where learners can express themselves fluently and spontaneously without much obvious searching for expressions. They can use language flexibly and effectively for social, academic, and professional purposes.",
        badge: "Advanced",
        content: fallbackC1Content
    },
    C2: {
        level: "C2 Level",
        description: "C2 is the mastery level, where learners can understand virtually everything heard or read with ease. They can summarize information from different sources, express themselves spontaneously, very fluently, and precisely in complex situations.",
        badge: "Proficiency",
        content: fallbackC2Content
    }
};
export const fallbackContentBanners: ContentBannerProps[] =
    Object.values(languageLevels).flatMap(l => l.content)

