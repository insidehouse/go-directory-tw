import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

import sitemap from '@astrojs/sitemap';

export default defineConfig({
  integrations: [tailwind(), sitemap()],
  // 正式網域：換網域只改這一行，再跑 npm run check
  site: 'https://weiqi.tw',
});