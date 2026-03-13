# Go Directory Taiwan

Taiwan Go (圍棋) school directory — Astro 5.3 + Tailwind static site.

## Build / Dev

- `npm run dev` — dev server
- `npm run build` — production build (~1.5s, 61 pages)

## Architecture

- 24 schools, 48 locations across 9 cities
- Combined `[id].astro` handles city slugs (english) + school slugs (chinese) at `/schools/[id]/`
- Client-side filtering on `/schools/` listing page (city + age group)
- Adults micro-directory at `/schools/adults/` with online platform alternatives
- Data source: `src/data/` (school JSON files)
- SEO: canonical URLs, OG tags, Schema.org EducationalOrganization, sitemap, robots.txt
