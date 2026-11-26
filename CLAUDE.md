# REF Builders website: Version 2 (Dark)

This is the handoff for continuing the **Version 2 (Dark)** build in Claude Code. It stands on its own and doesn't depend on the other version's folder.

- **Client:** REF Builders (RObedgardflam Corporation DBA REF Builders), a residential and commercial general contractor in Campbell, CA.
- **Podio item:** https://podio.com/outsource-plug/website-ticketing/apps/web-dev-accounts/items/95
- **Podio task (assigned to John Tubay):** https://podio.com/tasks/320005269, "REF Builders | Website Development"
- **Status:** first-build HTML prototype. All copy is a developer draft for Gelmarc's audit. Nothing is published. Not yet reviewed by Aryan, Mary or Anthony.
- **Sibling version:** Version 1 (Light), ref-builders-v1-light. It has the same layout and content; only the color theme differs.
- **Origin:** rebuilt Nov 26, 2026 from the v1-light generator (including its Nov 25 design refresh) with `THEME = "dark"`, replacing the older ref-builders-v2-dark.zip handoff, which predated that refresh. `build/` and `content.py` must stay in sync with v1: port generator or copy changes across, then rebuild both.

## Rules this build must follow
Every change must follow both workflows. Re-check the build against them before showing anything.
1. **Aryan's Developer Layout Workflow:** https://docs.google.com/document/d/13S1iT7avVAWgXMc8UTiTb_Lo_CzG9QJB3bpbaW4jy7E/edit (header, hero, homepage order, forms, footer, page types, legal).
2. **Gelmarc's SEO Workflow and page templates:** https://docs.google.com/document/d/1vcfNmyldq5y0H_mADSxokD2qe-twiWL6KUfbT4_yVi4/edit (section order per page, FAQ counts, metadata, headings).

The key rules already applied, which you should keep:
- **Pages:** exactly the 25 in the Podio Website Pages doc (https://docs.google.com/document/d/1zycOmfqc9XPYibUX6th_TFWyaJ3xFSQb4bzMpcVB1nY/edit), plus Privacy and Terms. Don't add pages.
- **Menu:** Home, About (with FAQs and Blogs in its dropdown), Services, Projects, Service Areas, Contact. Every parent has a dropdown. There is one header button, and it goes to `contact.html#form`.
- **Hero:** full-screen muted looping video with only an H1, a subtitle and one button.
- **Homepage order:** About, Why choose us, Services, How we work, Service areas, Featured projects, FAQ (10), then the footer form band. Professional Affiliations and Reviews are left out because nothing is verified for either.
- **FAQs:** 10 on every non-project page, 20 on `faqs.html`, and none on Projects or project pages.
- **Footer form band** on every page except Contact, which has its own form and no band.
- **Form:** two SMS boxes, non-marketing first. Both are required and start unticked, with the paid ads team's wording and daily frequency. Privacy and Terms links go under the submit button.
- **Footer credit, exactly:** `© 2026 REF Builders | Designed & Managed by Apex Operations`, with "Apex Operations" linking to https://apexops.agency.
- **Banned:** em dashes, hover zoom on images, tilted cards, marquees, a giant footer wordmark, and any fact that isn't in Podio.
- **Headings:** one H1 per page, no skipped levels. The generator sentence-cases H1 and H2.

## Verified facts (Podio onboarding form and brief only)
- Phone (831) 566-9040 (`tel:+18315669040`). Owner (669) 299-9204. Email refbuilders@gmail.com.
- Address: 710 E McGlincy Ln, Ste 109, Campbell, CA 95008.
- Instagram https://www.instagram.com/refbuilders/ and Yelp https://www.yelp.com/biz/ref-builders-campbell.
- Coverage: Santa Clara County, San Mateo County, Alameda County and San Francisco. City pages: Palo Alto, Stanford, Redwood City, Saratoga and Los Gatos.
- People: Roberto Flamenco (owner, 25+ years, rough construction) and Paula (finishes).
- Services (8): Full Home Remodeling, New Home Construction, Kitchen Remodeling, Bathroom Remodeling, Home Additions, ADU Construction, Commercial Construction & Tenant Improvements, Fire Restoration & Reconstruction.

## Project structure
```
ref-builders-v2-dark/
  CLAUDE.md              this handoff
  build/
    theme.py             THEME = "dark"
    content.py           all page copy: services, cities, projects, blog posts, FAQs
    build.py             static site generator; writes every page into ../site/
    make-hero-video.sh   turns a Drive drone clip into the hero video (needs ffmpeg)
  site/                  generated output; open site/index.html
    assets/css/site.css  design system (base, shared with v1)
    assets/css/dark.css  Version 2 overrides, loaded after site.css (palette, header, panels, forms, footer, service-area map)
    assets/js/site.js    menu, reveals, service explorer, accordion, slider, form validation
    assets/img/          webp photos (1800px and -sm 900px), logos, favicon, hero poster
    assets/video/ref-hero.mp4
```
**How to work:** edit copy in `build/content.py`, page markup in `build/build.py` and styles in `site/assets/css/`. Then run:
```
cd build && python3 build.py      # rebuilds all 27 HTML pages in ../site
```
On Windows, if the folder path is very long the build can fail with FileNotFoundError (260-character limit). Map a short drive first: `subst Q: <project folder>`, build from `Q:\build`, then `subst Q: /D`.
Don't hand-edit the generated `site/*.html` files, because the next build overwrites them.

## Design system (Version 2 (Dark))
**Version 2, dark:** the same components as v1 with `dark.css` layered on top. Palette: paper `#0f1110`, stone `#161917`, sand `#202421`, ink `#f2f0eb`, body text `#c9ccc7`, `.sec--dark` panels `#0a0b0b`, brand red `#d9161d` unchanged. White buttons (`.btn--light`), white logo in header and footer (`ref-logo-white.png`), dark glass header, and a dark-cartography version of the homepage service-area map. Any new component added in v1 needs a matching rule in `dark.css`.

**Near-square 5px corners (v2 only, Nov 26):** every corner is a small 5px radius (first fully square, then softened to 5px on feedback). The end of `dark.css` sets `--r-lg/--r-md/--r-sm` to 5px, forces `border-radius:5px` on all elements, gives the clip-path reveals (`ih-frame`, `.xcard`, `.wipe`, `.scard`) and the map labels the same 5px, and sets `--round:5`. `site.js` reads `--round` as a fixed px radius for the footer band's clip-path reveal; when it's unset (v1) the original 56 to 40px rounding is used. Port that `site.js` change to v1 to keep the shared JS identical. Map pins and their two legend dots stay round on purpose.

**Type (v2 only, Nov 26):** headings are **Anton**, all caps (client's pick); paragraphs are **Jost**, a refined geometric sans, with 1.7 line height. Montserrat, Archivo Expanded, Plus Jakarta Sans and Be Vietnam Pro were tried first. Anton has a single 400 weight, so heading weights are pinned to 400 and `font-synthesis-weight:none` stops faux bold. The generator loads both from Google Fonts when `THEME = "dark"`, and `--head`/`--body` point to them. Heading sizes are set per context in `dark.css` sets every heading context explicitly (sizes bumped ~25-30% on Nov 26 at the client's request). `.ihero h1` and `.faq__side h2` are capped so RECONSTRUCTION fits, and the `.scope`/`.card` titles drop to 17px on phones. When adding a heading style, check long words such as RECONSTRUCTION at 390px.

**Centered homepage hero (v2 only, Nov 26):** the eyebrow, H1, subtitle and button sit in one centered column near the bottom of the video, at the same bottom spacing as v1 (v1 keeps the bottom-left headline with the subtitle and button on the right). A soft radial shade behind the text keeps it readable. "to finish." in the H1 is a thick red outline (`.ol`, `-webkit-text-stroke` ~.035em); it sits outside the `<em>` because the em paints its red fill through every letter inside it.

**Wider sections, less padding (v2 only, Nov 26):** `dark.css` raises `--wrap` from 1360px to 1600px, cuts `--gutter` to 16-36px and `--sec` (section top/bottom padding) to 64-112px, pulls the inner-page dark panels and footer form band closer to the screen edge (8-14px), and widens the form band to 1680px.

For reference, Version 1 (Light):
**Version 1, light: "Modern architectural"** (inspired by Nuvo ADU and the Vericlean preview)
- Palette in `site.css` `:root`: paper `#f8f7f3`, stone `#efece6`, ink `#1c1f1d`, forest `#262b28` (dark panels), sage `#8a9a86` / `#5f6f5c`, and brand red `#d9161d` on buttons and badges only.
- Headings are Outfit 500. The second phrase in `<em>` is muted grey, for example "Built right. *From foundation to finish.*"
- Light sections alternate with stone sections that have a faint grid (`.grid-bg`). The map, featured projects and form band are dark rounded panels.
- In v1 the footer is light and uses the dark logo; in v2 it is `#0a0b0b` with the white logo.

Shared components (in `site.css`, defined once for both versions):
- Floating pill header with a blur effect. It's see-through over the home hero and becomes a dark bar once you scroll.
- Rounded corners: 28px for large panels, 20px for cards. Eyebrows are small pills with a red dot.
- Buttons are red pills with a dark arrow circle; `.btn--light` is the white variant.
- Home components: `.ab` (About, with a floating 25+ badge), `.vcards` (four staggered value cards), `.sx` (service explorer: hovering a tile swaps the large photo), `.scards` (six step cards with red number badges), `.mappanel` (dark map with a city list), `.inset` (featured-projects drone panel with glass cards).
- Motion: word-by-word heading reveals (`data-split`), rounded image reveals (`.wipe`), fade-ups (`.rv`) and light parallax (`data-para`). All of it respects reduced motion.
- Fonts: Outfit for headings and Inter for body, both from Google Fonts. There's no brand font guide, so the headings use a sans serif as the rules require.

## Open items before handoff or launch
1. **Hero video.** It's currently a slideshow built from the media-shoot photos. Download `DJI_20261117112411_0164_D.MP4` from the Drive drone folder (an 18-second descent toward the finished home). Then run `./build/make-hero-video.sh /path/to/DJI_..._0164_D.MP4 1 14`. The backup clip is `DJI_20261117112321_0163_D.MP4`.
2. **Logo.** There's no official file in Podio or Drive; the current one was captured from refbuilders.com. Ask Mary to get the vector file.
3. **Privacy and Terms.** REF has no entry in the paid ads master, so these adapt the standard contractor format. The paid ads team needs to review them, and the effective date is a placeholder.
4. **Project photos.** Both project placeholders use the Nov 17 shoot (one house), with the house number blurred. Replace them with Paula's organized Dropbox photos once they arrive, and confirm the project names with Gelmarc.
5. **Commercial and fire pages** use residential photos for now.
6. **License.** The logo shows LIC #977818, but Podio has no license field, so the license isn't shown anywhere else until Mary confirms it.
7. **Google Business Profile.** The link isn't confirmed as verified, so it's left out.
8. **Content route.** Gelmarc audits all copy; this is the developer draft.
9. **Branding check.** REF is pre-branded per Mary (Nov 9), so the build goes straight to the developer.

## Next steps (Aryan's workflow)
1. Present Version 1 (light) and Version 2 (dark) to Anthony as the two homepage directions, and get his pick.
2. Push the chosen version to an Apex GitHub org repo and deploy a staging preview on Vercel, Cloudflare Pages, Hostinger or GitHub Pages. Put both links in the Podio project fields and leave a Podio note each night.
3. Run QC (section 12 of Aryan's workflow) at 1440px, 768px and 390px: no console errors and no sideways scroll. Check that the menus and forms work, and aim for 90+ on accessibilitychecker.org.
4. Port to Duda: save a native Site Backup first. Use one HTML element per section, put the header and footer in Duda's global header and footer, CSS in site.css under Developer Mode, and media in the File Library. Wire the forms to a hidden Duda form with default notifications. **Never publish** until Aryan types "publish REF Builders".
5. Once it's on Duda, assign Gelmarc the content and SEO audit task.

## QC script idea
Playwright and Chromium work in Claude Code. Screenshot each page at 1440px and 390px and check:
- `document.documentElement.scrollWidth - innerWidth === 0`
- exactly one `<h1>` per page
- the FAQ count (`.acc__i`)
- that every internal `href` resolves to an existing file
