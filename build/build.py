# -*- coding: utf-8 -*-
"""Static site generator for the REF Builders prototype."""
import os, html, json, re
from content import *
from areamap import area_map
try:
    from theme import THEME
except ImportError:
    THEME = "light"
DARK = THEME == "dark"

OUT = os.path.join(os.path.dirname(__file__), "..", "site")
SVC = {s["slug"]: s for s in SERVICES}
CTY = {c["slug"]: c for c in CITIES}
E = html.escape

def ver(rel):
    """Short content hash so browsers load the new file after every change."""
    import hashlib
    with open(os.path.join(OUT, rel), "rb") as f: return hashlib.md5(f.read()).hexdigest()[:8]

ALT = {
 "drone-front":"Aerial front view of a new two-story stucco home with a gabled roof and landscaped yard",
 "drone-oblique":"Aerial view of a completed new home with solar panels, skylights and a fenced backyard",
 "drone-rear":"Aerial view of a new home's backyard patio and lawn surrounded by autumn trees",
 "drone-top":"Top-down aerial view of a new home's roof, skylights and backyard",
 "ext-front":"Front elevation of a new stucco home with dark trim, arched entry and carriage-style garage door",
 "ext-front-2":"Two-story home with steep gables, black-framed windows and a paver walkway",
 "ext-angle":"New stucco home viewed from the driveway with autumn leaves and exterior sconces",
 "ext-fence":"New home behind a split-rail fence with a young maple tree in the front yard",
 "ext-fence-2":"Front yard of a new home with a split-rail fence, lawn and stepping-stone path",
 "ext-rear-1":"Rear of a new home with wide glass doors, a concrete patio and a lawn",
 "ext-patio":"Backyard concrete patio and steps leading to sliding glass doors",
 "ext-yard":"Private backyard with lawn, mulched planting beds and a cedar lattice fence",
 "int-great-room":"Bright great room with wide-plank floors, recessed lights and a linear pendant",
 "int-open-plan":"Open-plan living area flowing into a modern kitchen with a waterfall island",
 "int-open-plan-2":"Open living space with skylights, a modern kitchen and glass doors to the yard",
 "int-kitchen":"Modern kitchen with a white waterfall island, wood cabinetry and a crystal chandelier",
 "int-kitchen-island":"Kitchen island with white stone waterfall edge, wood niche and statement chandelier",
 "int-kitchen-sink":"Kitchen island with a copper sink, black faucet and skylights above",
 "int-bath-vanity":"Bathroom with a gray shaker vanity, quartz top and lit medicine cabinet",
 "int-stair":"Curved staircase with wood treads and black metal balusters",
 "int-wetbar":"Upstairs wet bar with gray cabinets, wine fridge and range hood",
 "int-bedroom-vault":"Vaulted bedroom with a brass chandelier and clerestory window",
 "int-bedroom-2":"Bedroom with vaulted ceiling, brass chandelier and windows to autumn trees",
 "int-suite":"Primary suite with a candle-style chandelier and doorway to the bathroom",
 "int-room-3":"Sunlit bedroom with trimmed windows and light wood floors",
 "int-powder":"Powder room with marble-look tile, pedestal sink and round backlit mirror",
}

I = {
 "ar":'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4"/></svg>',
 "arl":'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M13 8H3M7 4 3 8l4 4"/></svg>',
 "up":'<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 12 12 4M5 4h7v7"/></svg>',
 "chev":'<svg viewBox="0 0 12 8" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m1 1 5 5 5-5"/></svg>',
 "phone":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2"/></svg>',
 "mail":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 "ig":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
 "yelp":'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.3 2.4c-.9-.2-4.6.9-5.3 1.5-.3.3-.4.6-.3 1l3.6 6.2c.6 1 2.1.6 2.1-.6V3.4c0-.5-.2-.9-.1-1zM9.5 14l-5 1.6c-.4.1-.6.5-.6.9.1 1 .9 3.4 1.6 4 .3.3.7.3 1 .2l3.9-3.6c.8-.8.2-2.1-.9-2zm1.8 1.7-.1 5.3c0 .4.3.8.7.8 1 .2 3.5-.2 4.2-.7.3-.2.4-.6.3-1l-3.2-4.6c-.6-.9-1.9-.6-1.9.2zm2.8-2.9 5 1.5c.4.1.8-.1.9-.5.4-.9.5-3.4.1-4.2-.2-.4-.6-.5-1-.4l-4.9 2c-1 .4-1 1.9-.1 1.6zm-.4-2.5 3.6-3.8c.3-.3.3-.7.1-1-.6-.8-2.8-2.1-3.8-2.1-.4 0-.7.3-.8.7l-.7 5.2c-.2 1.1 1 1.6 1.6 1z"/></svg>',
}

def img(name, alt=None, cls="", eager=False, sizes="(max-width: 960px) 100vw, 50vw", para=False):
    a = E(alt if alt is not None else ALT.get(name, ""))
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    p = ' data-para=".06"' if para else ""
    return (f'<img src="assets/img/{name}.webp" srcset="assets/img/{name}-sm.webp 900w, assets/img/{name}.webp 1800w" '
            f'sizes="{sizes}" alt="{a}" width="1800" height="1202" {load}{p}{(" class=%s" % chr(34)+cls+chr(34)) if cls else ""}>')

def btn(label="Start Your Project", href="contact.html#form", light=False):
    return f'<a class="btn{" btn--light" if light else ""}" href="{href}">{E(label)}<span class="ar">{I["up"]}</span></a>'

def link(label, href):
    return f'<a class="link-ar" href="{href}">{E(label)}{I["ar"]}</a>'

def eyebrow(t): return f'<span class="eyebrow rv">{E(t)}</span>'

def marquee():
    """Scrolling strip of every service, each with a pulsing red dot. The list is
    duplicated so the loop is seamless; the copy is hidden from screen readers."""
    links="".join(f'<li><a href="{x["slug"]}.html">{E(x["name"])}</a></li>' for x in SERVICES)
    copy="".join(f'<li>{E(x["name"])}</li>' for x in SERVICES)
    return f'''<section class="mq" aria-label="Our services"><div class="mq__track"><ul class="mq__list">{links}</ul><ul class="mq__list" aria-hidden="true">{copy}</ul></div></section>'''

def house(cls="", stretch=False):
    """The logo's house outline as a line drawing: open left wall, roof rising to the peak,
    right wall and base, drawn with two parallel lines like the logo. Draws itself in on reveal."""
    paths=["M6 168 V448 H352","M190 126 L417 6 L594 170 V448 H556",
           "M20 168 V434 H352","M200 140 L417 22 L580 176 V434 H556"]
    pp="".join(f'<path d="{d}" pathLength="1" style="--k:{i}"/>' for i,d in enumerate(paths))
    par = ' preserveAspectRatio="none"' if stretch else ""
    return f'<svg class="house roof-draw {cls}" viewBox="0 0 600 456"{par} aria-hidden="true" focusable="false">{pp}</svg>'

# ---------------------------------------------------------------- NAV
NAV = [
 ("Home","index.html",[]),
 ("About","about.html",[("About REF Builders","about.html"),("FAQs","faqs.html"),("Blogs","blog.html")]),
 ("Services","services.html",[(s["name"], s["slug"]+".html") for s in SERVICES]+[("All Services","services.html")]),
 ("Projects","projects.html",[(p["name"], p["slug"]+".html") for p in PROJECTS]+[("All Projects","projects.html")]),
 ("Service Areas","service-areas.html",[(c["name"], c["slug"]+".html") for c in CITIES]+[("All Service Areas","service-areas.html")]),
 ("Contact","contact.html",[]),
]

def header(active, inner=False):
    lis=[]
    for i,(name,href,sub) in enumerate(NAV):
        cur = ' aria-current="page"' if active==name else ""
        if sub:
            dd="".join(f'<a href="{h}"{" class=%sdd__all%s" % (chr(34),chr(34)) if n.startswith("All ") or n=="About REF Builders" and False else ""}>{E(n)}</a>' for n,h in sub)
            lis.append(f'<li class="has-dd"><a class="nav__a" href="{href}"{cur} aria-haspopup="true" aria-expanded="false">{name}{I["chev"]}</a><div class="dd" role="menu">{dd}</div></li>')
        else:
            lis.append(f'<li><a class="nav__a" href="{href}"{cur}>{name}</a></li>')
    m=[]
    for name,href,sub in NAV:
        if sub:
            items="".join(f'<a href="{h}">{E(n)}</a>' for n,h in sub)
            m.append(f'<li><div class="mnav__row"><a href="{href}">{name}</a><button class="mnav__tg" aria-expanded="false" aria-label="Show {name} pages">{I["chev"]}</button></div><div class="mnav__sub"><div>{items}</div></div></li>')
        else:
            m.append(f'<li><div class="mnav__row"><a href="{href}">{name}</a></div></li>')
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr{" is-inner" if inner else ""}">
  <div class="hdr__bar">
    <a class="hdr__logo" href="index.html" aria-label="REF Builders home"><img class="l-light" src="assets/img/ref-logo-white.png" alt="REF Builders" width="588" height="542"><img class="l-dark" src="assets/img/ref-logo.png" alt="REF Builders" width="588" height="542"></a>
    <nav class="nav" aria-label="Main"><ul>{"".join(lis)}</ul></nav>
    <a class="hdr__tel" href="tel:{BIZ["tel"]}">{I["phone"]}{BIZ["phone"]}</a>
    <span class="hdr__cta">{btn("Start a Project")}</span>
    <button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
  </div>
</header>
<nav class="mnav" id="mnav" aria-label="Mobile"><ul>{"".join(m)}</ul>
  <div class="mnav__foot"><a class="hdr__tel" href="tel:{BIZ["tel"]}">{I["phone"]}{BIZ["phone"]}</a>{btn("Start a Project")}</div>
</nav>'''

def head(title, desc, canon):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="https://www.refbuilders.com/{canon}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="assets/img/drone-front.webp">
<meta name="theme-color" content="{"#0f1110" if DARK else "#f8f7f3"}">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@200;300;400;500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={ver("assets/css/site.css")}">{chr(10)+'<link rel="stylesheet" href="assets/css/dark.css?v='+ver("assets/css/dark.css")+'">' if DARK else ""}
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"GeneralContractor","name":"REF Builders","telephone":"+1-831-566-9040","email":BIZ["email"],"url":"https://www.refbuilders.com/","address":{"@type":"PostalAddress","streetAddress":"710 E McGlincy Ln, Ste 109","addressLocality":"Campbell","addressRegion":"CA","postalCode":"95008","addressCountry":"US"},"areaServed":["Santa Clara County","San Mateo County","Alameda County","San Francisco"],"sameAs":[BIZ["instagram"],BIZ["yelp"]]})}</script>
</head>
<body>'''

SERVICE_OPTS = "".join(f'<option>{E(s["name"])}</option>' for s in SERVICES)

def form(fid, dark=True, btn_label="Send Inquiry"):
    c="form--dark" if dark else ""
    return f'''<form class="form {c}" id="{fid}" novalidate aria-label="Project inquiry form">
  <div class="fld"><label for="{fid}-fn">First name *</label><input id="{fid}-fn" name="first_name" autocomplete="given-name" required></div>
  <div class="fld"><label for="{fid}-ln">Last name *</label><input id="{fid}-ln" name="last_name" autocomplete="family-name" required></div>
  <div class="fld"><label for="{fid}-ph">Phone *</label><input id="{fid}-ph" name="phone" type="tel" autocomplete="tel" required></div>
  <div class="fld"><label for="{fid}-em">Email *</label><input id="{fid}-em" name="email" type="email" autocomplete="email" required></div>
  <div class="fld"><label for="{fid}-city">Project city *</label><input id="{fid}-city" name="city" autocomplete="address-level2" required placeholder="e.g. Palo Alto"></div>
  <div class="fld"><label for="{fid}-svc">Service *</label><select id="{fid}-svc" name="service" required><option value="">Select a service</option>{SERVICE_OPTS}<option>Other or not sure yet</option></select></div>
  <div class="fld full"><label for="{fid}-msg">Tell us about your project</label><textarea id="{fid}-msg" name="message" placeholder="Project type, timing, and whether you already have plans"></textarea></div>
  <label class="optin full"><input type="checkbox" name="sms_non_marketing" value="yes" required> <span>By checking this box, I consent to receive non-marketing text messages from REF Builders related to my inquiry, appointments, estimates, and service updates. Message frequency: daily. Message and data rates may apply. Reply HELP for help or STOP to opt out.</span></label>
  <label class="optin full"><input type="checkbox" name="sms_marketing" value="yes" required> <span>By checking this box, I consent to receive marketing text messages about special offers, discounts, and new product updates from REF Builders at the phone number provided. Message frequency: daily. Message and data rates may apply. Text HELP for assistance, reply STOP to opt out.</span></label>
  <div class="full">{'<button class="btn btn--light" type="submit">' if dark else '<button class="btn" type="submit">'}{btn_label}<span class="ar">{I["up"]}</span></button></div>
  <p class="form__legal full"><a href="privacy-policy.html">Privacy Policy</a> &nbsp;|&nbsp; <a href="terms-and-conditions.html">Terms and Conditions</a></p>
  <div class="form__ok full" role="status" tabindex="-1">Thank you. Your inquiry has been received and we will be in touch soon.</div>
</form>'''

def band(h2="Let's Talk About Your Project", sub="Tell us what you are planning. We will review the details and reach out to set up a time to talk."):
    contacts=[
        ("phone","Call us",BIZ["phone"],f'tel:{BIZ["tel"]}'),
        ("mail","Email",BIZ["email"],f'mailto:{BIZ["email"]}'),
        ("pin","Visit the office",f'{BIZ["addr1"]}, {BIZ["addr2"]}',"https://www.google.com/maps/search/?api=1&query="+BIZ["addr1"].replace(" ","+")+",+"+BIZ["addr2"].replace(" ","+")),
    ]
    cards="".join(f'<a class="fcon" href="{h}"{" target=%s_blank%s rel=%snoopener%s" % ((chr(34),)*4) if h.startswith("http") else ""}><span class="fcon__i">{I[i]}</span><span class="fcon__t"><small>{E(l)}</small><b>{E(v)}</b></span><span class="fcon__go">{I["up"]}</span></a>' for i,l,v,h in contacts)
    return f'''<section class="fband" aria-labelledby="band-h"><div class="fband__panel">
  <div class="fband__bg" aria-hidden="true">{img("ext-front-2", alt="", sizes="100vw")}</div>
  {house("house--band")}
  <div class="wrap fband__g">
    <div class="fband__intro">
      {eyebrow("Start a project")}
      <h2 id="band-h" data-split>{E(h2)}</h2>
      <p class="lede rv" style="--d:1">{E(sub)}</p>
      <div class="fband__info rv" style="--d:2">{cards}</div>
    </div>
    <div class="fband__form rv" style="--d:1">
      <div class="fcard">
        <div class="fcard__head"><h3>Request a consultation</h3><p>Fields marked * are required.</p></div>
        {form("inquiry")}
      </div>
    </div>
  </div>
</div></section>'''

def footer(with_band=True, band_h2=None, band_sub=None):
    b = band(*( [band_h2] + ([band_sub] if band_sub else []) )) if (with_band and band_h2) else (band() if with_band else "")
    svc="".join(f'<li><a href="{s["slug"]}.html">{E(s["name"])}</a></li>' for s in SERVICES)
    prj="".join(f'<li><a href="{p["slug"]}.html">{E(p["name"])}</a></li>' for p in PROJECTS)
    return f'''{b}
<footer class="ftr">
  <div class="wrap">
    <div class="ftr__g">
      <div>
        <img class="ftr__logo" src="assets/img/{"ref-logo-white.png" if DARK else "ref-logo.png"}" alt="REF Builders" width="588" height="542" loading="lazy">
        <ul class="ftr__contact">
          <li>{I["phone"]}<a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a></li>
          <li>{I["mail"]}<a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></li>
          <li>{I["pin"]}<span>{BIZ["addr1"]}<br>{BIZ["addr2"]}</span></li>
        </ul>
        <div class="ftr__social">
          <a href="{BIZ["instagram"]}" target="_blank" rel="noopener" aria-label="REF Builders on Instagram">{I["ig"]}</a>
          <a href="{BIZ["yelp"]}" target="_blank" rel="noopener" aria-label="REF Builders on Yelp">{I["yelp"]}</a>
        </div>
      </div>
      <div><h3>Company</h3><ul><li><a href="index.html">Home</a></li><li><a href="about.html">About</a></li><li><a href="faqs.html">FAQs</a></li><li><a href="blog.html">Blogs</a></li><li><a href="service-areas.html">Service Areas</a></li><li><a href="contact.html">Contact</a></li></ul></div>
      <div><h3>Services</h3><ul>{svc}</ul></div>
      <div><h3>Projects</h3><ul>{prj}<li><a href="projects.html">All Projects</a></li></ul></div>
      <div><h3>Our Office</h3><div class="ftr__map"><iframe title="Map of REF Builders office in Campbell, CA" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=710+E+McGlincy+Ln+Ste+109,+Campbell,+CA+95008&amp;z=11&amp;output=embed"></iframe></div></div>
    </div>
    <div class="ftr__bot">
      <p style="margin:0">&copy; 2026 REF Builders | Designed &amp; Managed by <a href="https://apexops.agency" target="_blank" rel="noopener">Apex Operations</a></p>
      <ul><li><a href="privacy-policy.html">Privacy Policy</a></li><li><a href="terms-and-conditions.html">Terms and Conditions</a></li><li><button type="button" class="termly-display-preferences">Cookie Preferences</button></li></ul>
    </div>
  </div>
</footer>
<script src="assets/js/site.js?v={ver("assets/js/site.js")}" defer></script>
</body>
</html>'''

def faq_block(faqs, h2="Frequently Asked Questions", lead=None, eyebrow_t="FAQs", stone=False, side_extra=""):
    items="".join(f'''<div class="acc__i"><h3 class="acc__h"><button class="acc__q" aria-expanded="false"><span>{E(q)}</span><span class="acc__ic" aria-hidden="true"></span></button></h3><div class="acc__a"><div><p>{E(a)}</p></div></div></div>''' for q,a in faqs)
    lead = lead or "Straight answers about how we work. If your question is not here, call us or send a message."
    return f'''<section class="sec{" sec--stone" if stone else ""}" aria-labelledby="faq-h">
  <div class="wrap faq">
    <div class="faq__side">{eyebrow(eyebrow_t)}<h2 id="faq-h" data-split>{E(h2)}</h2><p class="lede rv">{E(lead)}</p>{side_extra}<div class="rv" style="--d:2;margin-top:28px">{link("Ask us a question","contact.html#form")}</div></div>
    <div class="acc rv">{items}</div>
  </div>
</section>'''

def phero(h1, sub, image, crumbs, cta=True, eb=None):
    cr='<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a>'+"".join(f'<span aria-hidden="true">/</span>'+(f'<a href="{h}">{E(n)}</a>' if h else f'<span aria-current="page">{E(n)}</span>') for n,h in crumbs)+'</nav>'
    kicker = eb or crumbs[0][0]
    tags = [crumbs[0][0], "Campbell, CA"]
    return f'''<section class="ihero" aria-label="Page introduction">
  <div class="ihero__bg" aria-hidden="true">{img(image, alt="", eager=True, sizes="100vw")}</div>
  <div class="wrap ihero__g">
    <div class="ihero__copy">
      {house("house--hero", stretch=True)}
      {cr}
      <span class="ihero__kicker">{E(kicker)}</span>
      <h1 data-split>{E(h1)}</h1>
      <p class="ihero__lead">{E(sub)}</p>
      {('<div class="ihero__btn">'+btn()+'</div>') if cta else ""}
    </div>
    <div class="ihero__frame">
      <div class="ihero__ph">{img(image, eager=True, sizes="(max-width:960px) 100vw, 46vw")}</div>
      <div class="ihero__tags" aria-hidden="true">{"".join(f"<span>{E(t)}</span>" for t in tags)}</div>
      <!--TOC-->
    </div>
  </div>
</section>'''

def strip(text="Talk with Roberto and Paula about your project.", image="int-kitchen", label="Start Your Project"):
    """Slim dark call-to-action pill placed mid-page on inner pages."""
    return f'''<section class="cstrip-sec" aria-label="Start a project"><div class="wrap"><div class="cstrip rv"><span class="cstrip__th">{img(image, alt="", sizes="90px")}</span><p class="cstrip__t">{E(text)}</p>{btn(label)}</div></div></section>'''

def svc_cards(slugs=None, cols=4, numbered=True):
    out=[]
    for i,s_ in enumerate([SVC[x] for x in (slugs or [s["slug"] for s in SERVICES])]):
        n = f'<span class="xcard__n">{i+1:02d}</span>' if numbered else ""
        out.append(f'''<article class="xcard" style="--d:{i%4}"><a class="card__cover" href="{s_["slug"]}.html" aria-label="View Service: {E(s_["name"])}"></a><div class="xcard__img">{img(s_["img"], sizes="(max-width:640px) 100vw, (max-width:1240px) 50vw, 25vw")}</div>{n}<div class="xcard__panel"><span class="xcard__meta">Service</span><h3 class="xcard__t">{E(s_["name"])}</h3><p class="xcard__lead">{E(s_["short"])}</p><span class="xcard__go" aria-hidden="true">{I["up"]}</span></div></article>''')
    return f'<div class="xcards{" xcards--3" if cols==3 else ""}">{"".join(out)}</div>'

def svc_explorer():
    res=[s_ for s_ in SERVICES[:6]]; com=SERVICES[6:]
    def tile(s_,i):
        return f'<a class="sx__tile" href="{s_["slug"]}.html" data-img="assets/img/{s_["img"]}.webp" data-name="{E(s_["name"])}" data-short="{E(s_["short"])}"><span class="sx__thumb">{img(s_["img"], sizes="220px")}</span><span class="sx__name">{E(s_["name"])}</span><span class="sx__go" aria-hidden="true">{I["up"]}</span></a>'
    first=SERVICES[0]
    return f'''<div class="sx rv">
  <div class="sx__feat"><img src="assets/img/{first["img"]}.webp" alt="" class="sx__big" loading="lazy" width="1800" height="1202"><div class="sx__cap"><span class="pill-badge">{len(SERVICES)} services</span><h3 class="sx__h">{E(first["name"])}</h3><p class="sx__p">{E(first["short"])}</p></div></div>
  <div class="sx__list">
    <div class="sx__grp"><h3 class="sx__gh">Residential construction & remodeling <span>{len(res)}</span></h3><div class="sx__grid">{"".join(tile(x,i) for i,x in enumerate(res))}</div></div>
    <div class="sx__grp"><h3 class="sx__gh">Commercial & restoration <span>{len(com)}</span></h3><div class="sx__grid">{"".join(tile(x,i) for i,x in enumerate(com))}</div></div>
  </div>
</div>'''

def proj_slider(items=None, h2="Featured Projects", lede="A look at recent work, from structure to finish. Every project page shows that project's own photos."):
    items = items or PROJECTS
    cards="".join(f'''<article class="pcard"><a href="{p["slug"]}.html" class="card__cover" aria-label="View project: {E(p["name"])}"></a><div class="pcard__img">{img(p["img"], sizes="(max-width:640px) 90vw, 780px")}</div><div class="pcard__b"><div><span class="tag">{E(p["type"])}</span><h3>{E(p["name"])}</h3></div><span class="btn btn--light" aria-hidden="true">View Project<span class="ar">{I["up"]}</span></span></div></article>''' for p in items)
    return f'''<div class="head-row"><div>{eyebrow("Projects")}<h2 data-split>{E(h2)}</h2></div><div><p class="lede rv">{E(lede)}</p><div class="pctl rv" style="margin-top:24px"><button data-prev aria-label="Previous project">{I["arl"]}</button><button data-next aria-label="Next project">{I["ar"]}</button></div></div></div>
<div class="pslider rv"><div class="ptrack">{cards}</div><div class="pbar"><i></i></div></div>'''

def county_map():
    # schematic coverage diagram (not to scale)
    return '''<div class="cmap rv" role="img" aria-label="Schematic map of REF Builders coverage: San Francisco, San Mateo County, Alameda County and Santa Clara County, with the office in Campbell">
<svg viewBox="0 0 500 520">
  <path class="bay" d="M150 20 C190 60 205 120 232 180 C255 230 300 260 330 300 C342 318 330 330 312 322 C270 300 230 258 205 214 C180 170 160 110 138 60 Z"/>
  <path class="cty" d="M70 30 L150 20 L160 70 L95 82 Z"/>
  <path class="cty on" d="M95 82 L160 70 C175 120 192 170 212 210 C230 245 255 268 280 290 L235 330 L170 300 L120 230 L80 150 Z"/>
  <path class="cty on" d="M232 180 C228 120 240 60 300 40 L440 60 L460 200 L400 250 L330 300 C300 262 255 230 232 180 Z"/>
  <path class="cty on" d="M170 300 L235 330 L280 290 L330 300 L400 250 L460 200 L480 330 L430 470 L300 500 L200 430 Z"/>
  <text x="76" y="58">SF</text>
  <text x="96" y="190">San Mateo</text>
  <text x="330" y="140">Alameda</text>
  <text x="300" y="420">Santa Clara</text>
  <g class="pin"><circle class="r" cx="182" cy="232" r="7"/><circle class="c" cx="182" cy="232" r="4.5"/><text x="194" y="236">Redwood City</text></g>
  <g class="pin"><circle class="r" cx="222" cy="290" r="7"/><circle class="c" cx="222" cy="290" r="4.5"/><text x="152" y="282">Palo Alto</text></g>
  <g class="pin"><circle class="r" cx="210" cy="312" r="7"/><circle class="c" cx="210" cy="312" r="4.5"/><text x="146" y="330">Stanford</text></g>
  <g class="pin"><circle class="r" cx="292" cy="402" r="7"/><circle class="c" cx="292" cy="402" r="4.5"/><text x="222" y="400">Saratoga</text></g>
  <g class="pin"><circle class="r" cx="330" cy="420" r="7"/><circle class="c" cx="330" cy="420" r="4.5"/><text x="340" y="446">Los Gatos</text></g>
  <g class="pin pin--hq"><circle class="c" cx="336" cy="384" r="5"/><text x="348" y="380">Campbell office</text></g>
</svg></div>'''

def county_list(dark=True):
    out=[]
    for name, slugs, others in COUNTIES:
        chips="".join(f'<a class="chip" href="{s}.html">{CTY[s]["name"]}</a>' for s in slugs)+"".join(f'<span class="chip">{E(o)}</span>' for o in others)
        out.append(f'<div class="county rv"><h3>{E(name)}</h3><div class="chips">{chips}</div></div>')
    return f'<div class="counties">{"".join(out)}</div>'

def steps_block(steps, eb="How we work", h2="A Clear Process From First Meeting to Final Finish", lede="Every project follows the same honest sequence. You always know what is happening now, what comes next and what we need from you.", image="int-stair", stone=True):
    st="".join(f'<div class="step"><span class="step__dot">{i+1:02d}</span><span class="tag">Step {i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(t,d) in enumerate(steps))
    return f'''<section class="sec{" sec--stone" if stone else ""}" aria-labelledby="proc-h"><div class="wrap proc">
  <div class="proc__stick">{eyebrow(eb)}<h2 id="proc-h" data-split>{E(h2)}</h2><p class="lede rv">{E(lede)}</p><div class="img proc__img wipe">{img(image)}</div></div>
  <div class="steps"><div class="steps__rail"><div class="steps__fill"></div></div>{st}</div>
</div></section>'''

STEP_IMG=["ext-front-2","int-great-room","drone-rear","int-kitchen","int-wetbar","int-kitchen-island"]
def steps_cards(steps, eb="How we work", h2="Clear steps. <em>No surprises.</em>", lede="Every project follows the same honest sequence. You always know what is happening now, what comes next and what we need from you."):
    items="".join(f'<article class="scard rv" style="--d:{i%3}"><div class="scard__img">{img(STEP_IMG[i%6], sizes="(max-width:960px) 100vw, 30vw")}<span class="scard__n">{i+1:02d}</span></div><div class="scard__b"><span class="tag">Step {i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div></article>' for i,(t,d) in enumerate(steps))
    return f'''<section class="sec sec--stone grid-bg" aria-labelledby="proc-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow(eb)}<h2 id="proc-h" data-split>{h2}</h2></div><p class="lede rv">{E(lede)}</p></div>
  <div class="scards">{items}</div>
</div></section>'''

STACK_IMG=["ext-front-2","int-great-room","drone-rear","int-kitchen","int-wetbar","int-kitchen-island"]
def stack_block(steps, eb="How we work", h2='A clear process, <em>start to finish</em>', lede="Every project follows the same honest sequence. You always know what is happening now, what comes next and what we need from you."):
    items="".join(f'<article class="stack__i" style="--k:{i}"><div><span class="num">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div><div class="img">{img(STACK_IMG[i%len(STACK_IMG)], sizes="(max-width:960px) 100vw, 45vw")}</div></article>' for i,(t,d) in enumerate(steps))
    return f'''<section class="sec sec--stone" aria-labelledby="proc-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow(eb)}<h2 id="proc-h" data-split>{h2}</h2></div><p class="lede rv">{E(lede)}</p></div>
  <div class="stack">{items}</div>
</div></section>'''

KEEP=["REF Builders","REF","Roberto Flamenco","Roberto","Paula","Palo Alto","Stanford","Redwood City","Saratoga","Los Gatos","Bay Area","Campbell","San Francisco","Santa Clara County","San Mateo County","Alameda County","Santa Clara","San Mateo","Alameda","South Bay","ADU","ADUs","FAQs","TI","Hillsborough","San Jose","Fremont","Peninsula"]
def _sent(txt):
    # sentence case for display headings, keeping proper nouns
    out=[];first=True
    for tok in re.split(r'(\s+)',txt):
        if not tok.strip() or tok.startswith('<') : out.append(tok); continue
        out.append(tok); 
    t="".join(out)
    marks={}
    for i,k in enumerate(sorted(KEEP,key=len,reverse=True)):
        key=f"\x00{i}\x00"
        if k in t: t=t.replace(k,key); marks[key]=k
    t=t.lower()
    # capitalize first letter of text and after ? or .
    t=re.sub(r'(^|[?.!]\s+)([a-z])',lambda m:m.group(1)+m.group(2).upper(),t)
    for key,k in marks.items(): t=t.replace(key,k)
    t=re.sub(r"\bi\b","I",t)
    return t
def sentence_headings(html_s):
    def fix(m):
        inner=m.group(2)
        parts=re.split(r'(<[^>]+>)',inner)
        first=True;res=[]
        for part in parts:
            if part.startswith('<'): res.append(part); continue
            if not part.strip(): res.append(part); continue
            t=_sent(part)
            if not first and t[:1].isupper() and part[:1].islower(): t=t
            if not first: t=t[:1]+t[1:]
            if not first and not part[:1].isupper(): t=t
            if not first: t=(part[:1] if part[:1] in " " else t[:1].lower() if part[:1].islower() else t[:1])+t[1:]
            first=False;res.append(t)
        return m.group(1)+"".join(res)+m.group(3)
    return re.sub(r'(<h[12][^>]*>)(.*?)(</h[12]>)',fix,html_s,flags=re.S)

def toc(s):
    """'On this page' list for the inner hero, built from the section H2s inside <main>."""
    if "<!--TOC-->" not in s: return s
    main = s.split('<main id="main">',1)[1].split("</main>",1)[0]
    items = [(i, re.sub(r"<[^>]+>","",t).strip()) for i,t in re.findall(r'<h2 id="([\w-]+)"[^>]*>(.*?)</h2>', main)][:5]
    if len(items) < 2: return s.replace("<!--TOC-->","")
    lis = "".join(f'<li><a href="#{i}"><span>{n+1:02d}</span>{t}</a></li>' for n,(i,t) in enumerate(items))
    return s.replace("<!--TOC-->", f'<nav class="ihero__toc" aria-label="On this page"><span class="ihero__tochead">On this page</span><ol>{lis}</ol></nav>')

def write(fn, s):
    s = sentence_headings(s)
    s = s.replace("—", ",").replace("–", "-")
    s = toc(s)
    # button labels: wrap text so it can roll on hover (the copy in data-t rises into place)
    s = re.sub(r'(<(?:a|button|span) class="btn[^"]*"[^>]*>)([^<]+)(<span class="ar">)', lambda m: f'{m.group(1)}<span class="btn__t" data-t="{m.group(2).strip()}"><span>{m.group(2)}</span></span>{m.group(3)}', s)
    # dark panels: darkened project photo with a red glow behind the content, plus the house-line watermark
    DARK_BG=["drone-front","ext-angle","int-great-room","drone-oblique","ext-front","int-open-plan-2","ext-rear-1","int-kitchen-island"]
    pick=sum(map(ord,fn))
    cnt=[0]
    def darkbg(m):
        name=DARK_BG[(pick+cnt[0])%len(DARK_BG)]; cnt[0]+=1
        return m.group(1)+f'<div class="dbg" aria-hidden="true">{img(name, alt="", sizes="100vw")}</div>'+house("house--dark")
    s = re.sub(r'(<section class="sec sec--dark"[^>]*>)', darkbg, s)
    if fn != "index.html": s = s.replace("<body>", '<body class="inner">', 1)
    with open(os.path.join(OUT, fn), "w", encoding="utf-8", newline="\n") as f: f.write(s)

# ================================================================ PAGES
HOME_FAQ=[
 ("What types of projects does REF Builders take on?","New homes, full home remodels, kitchen and bathroom remodels, home additions, ADUs, commercial construction and tenant improvements, and fire restoration and reconstruction."),
 ("Where is REF Builders located?","Our office is at 710 E McGlincy Ln, Ste 109 in Campbell, CA. We serve Santa Clara County, San Mateo County, Alameda County and San Francisco."),
 ("Do I need plans before I call you?","No. We can introduce you to architect and engineering partners, support the design and engineering process, and begin construction once your plans are approved."),
 ("Who runs REF Builders?","REF Builders is led by Roberto Flamenco and Paula. Roberto focuses on rough construction, foundations, framing and engineering coordination, and Paula coordinates finishes."),
 ("How do you keep clients informed?","Before each phase we explain what is happening, the expected dates and which selections are due. You can reach Roberto and Paula directly."),
 ("When do I need to choose finishes?","Some choices are needed early. Bathroom valves and kitchen layouts, for example, are required during rough plumbing. We give you a list of deadlines tied to each phase."),
 ("How do you handle changes during the project?","We discuss every change with you, explain the effect on the work and document it in writing before it is done."),
 ("Can I see your work before hiring you?","Yes. We share current projects, photos and videos so you can judge our construction and finishes."),
 ("Do you offer support after the project is complete?","Yes. Covered warranty issues are handled under the terms documented in your agreement."),
 ("How do I start a project with REF Builders?","Call us at (831) 566-9040 or send the inquiry form with your project city, the type of work and any plans you have."),
]

VAL_IMG=['int-powder', 'int-kitchen-island', 'int-stair', 'ext-rear-1']
def page_home():
    areas_intro="We work across four Bay Area regions from our office in Campbell, with dedicated pages for the communities we serve most."
    s=head("General Contractor in Campbell, CA | REF Builders","REF Builders builds new homes, remodels, additions and ADUs across Santa Clara, San Mateo and Alameda counties and San Francisco.","")
    s+=header("Home", inner=False)
    s+=f'''<main id="main">
<section class="hero" aria-label="Introduction">
  <div class="hero__media"><video data-auto autoplay muted loop playsinline preload="metadata" poster="assets/img/hero-poster.jpg" aria-hidden="true"><source src="assets/video/ref-hero.mp4" type="video/mp4"></video></div>
  <div class="wrap hero__in">
    <div class="hero__grid">
      <div class="hero__head">{eyebrow("General Contractor in Campbell, CA")}<h1 data-split>Built right. <em>From foundation to finish.</em></h1></div>
      <div class="hero__side"><p class="hero__sub rv" style="--d:4">New homes, remodels, additions and ADUs across the Bay Area, led by Roberto and Paula with honest communication at every phase.</p><div class="rv" style="--d:5">{btn("Start Your Project", light=True)}</div></div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="about-h"><div class="wrap ab">
  <div class="ab__txt">
    {eyebrow("About REF Builders")}
    <h2 id="about-h" data-split>One team, from foundation <em>to final finish.</em></h2>
    <p class="lede rv">REF Builders is a residential and commercial general contractor in Campbell, led by Roberto Flamenco and Paula.</p>
    <p class="rv muted">Roberto began in construction after arriving in the United States at 17 and brings more than 25 years of hands-on experience in foundations, framing and engineering coordination. Paula coordinates the finishes that bring a completed property together.</p>
    <div class="ab__duo rv"><div><span class="pill-badge">The rough</span><b>Roberto</b><small>Foundations, framing, engineering</small></div><div><span class="pill-badge">The finish</span><b>Paula</b><small>Finishes, selections, details</small></div></div>
    <div class="rv">{btn("Meet Roberto and Paula","about.html")}</div>
  </div>
  <div class="ab__media">
    {house("house--ab", stretch=True)}
    <div class="img ab__a wipe">{img("ext-front-2", para=True, sizes="(max-width:960px) 100vw, 45vw")}</div>
    <div class="img ab__b wipe" style="transition-delay:.2s">{img("int-kitchen", sizes="(max-width:960px) 60vw, 22vw")}</div>
    <div class="ab__stat rv" style="--d:3"><b><span data-count="25">25</span>+</b><small>years of hands-on construction experience</small></div>
  </div>
</div></section>

{marquee()}

<section class="sec sec--stone grid-bg" aria-labelledby="why-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Why choose us")}<h2 id="why-h" data-split>Four commitments. <em>One standard on every job.</em></h2></div><p class="lede rv">We would rather tell you the truth and fix a problem than sell you an image.</p></div>
  <div class="vcards">{"".join(f'<article class="vcard rv" style="--d:{i}"><div class="vcard__img">{img(VAL_IMG[i], sizes="(max-width:960px) 50vw, 25vw")}</div><div class="vcard__b"><span class="vcard__n">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div></article>' for i,(t,d) in enumerate(WHY))}</div>
</div></section>

<section class="sec" aria-labelledby="svc-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Services")}<h2 id="svc-h" data-split>Find your service. <em>From the foundation up.</em></h2></div><div><p class="lede rv">Eight residential and commercial services, each delivered with the same care for structure and finish.</p><div class="rv" style="margin-top:22px">{link("All services","services.html")}</div></div></div>
  {svc_explorer()}
</div></section>

{steps_cards(PROCESS)}

<section class="sec" aria-labelledby="areas-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Service areas")}<h2 id="areas-h" data-split>Your neighborhood. <em>Our home ground.</em></h2></div><p class="lede rv">{areas_intro}</p></div>
  <div class="mappanel rv">
    {area_map()}
    <div class="mapside">
      <div class="mapcard"><div class="img">{img("drone-oblique", sizes="(max-width:960px) 100vw, 30vw")}</div><span class="pill-badge pill-badge--glass">Office in Campbell</span><h3>Four Bay Area regions</h3><p>Santa Clara County, San Mateo County, Alameda County and San Francisco.</p>{btn("View Service Areas","service-areas.html", light=True)}</div>
      <div class="mapcard mapcard--list"><h3>Where is your project?</h3>{county_list()}</div>
    </div>
  </div>
</div></section>

<section class="sec sec--tight" aria-labelledby="proj-h"><div class="wrap wrap--wide">
  <div class="inset">
    <div class="inset__bg">{img("drone-rear", sizes="100vw", para=True)}</div>
    <div class="inset__top">{eyebrow("Featured projects")}<h2 id="proj-h" data-split>Real work. <em>Built to be seen up close.</em></h2></div>
    <div class="inset__cards">{"".join(f'<a class="glass rv" style="--d:{i}" href="{p["slug"]}.html"><span class="glass__img">{img(p["img"], sizes="140px")}</span><span class="glass__t"><span class="tag">{E(p["type"])}</span><b>{E(p["name"])}</b><span class="glass__go">View Project {I["ar"]}</span></span></a>' for i,p in enumerate(PROJECTS))}<a class="glass glass--all rv" style="--d:2" href="projects.html"><span class="glass__t"><span class="tag">Portfolio</span><b>All projects</b><span class="glass__go">View all {I["ar"]}</span></span></a></div>
  </div>
</div></section>

{faq_block(HOME_FAQ, stone=True)}
</main>'''
    s+=footer(True,"Ready to Start? Let's Talk About Your Project","Tell us what you are planning. We will review the details and reach out to set up a time to talk.")
    write("index.html", s)

ABOUT_FAQ=[
 ("Who owns REF Builders?","REF Builders is led by Roberto Flamenco, the owner, together with Paula. They work closely as a couple and as a team."),
 ("How long has Roberto worked in construction?","Roberto has more than 25 years of personal construction experience, beginning after he arrived in the United States at age 17."),
 ("What does Roberto focus on?","Roberto focuses on rough construction: foundations, framing and coordination with engineers."),
 ("What does Paula focus on?","Paula coordinates the finishes, starting after insulation and drywall, and the details that bring the completed property together."),
 ("Is REF Builders a general contractor?","Yes. REF Builders works as a general contractor and, where applicable, as a subcontractor."),
 ("Do you work with architects and engineers?","Yes. Architectural and engineering partners prepare designs and plans, and we guide clients through those relationships and the construction."),
 ("What values guide your work?","Quality finishes, honest communication, accountability, responsiveness and attention to detail."),
 ("What happens if something goes wrong on my project?","We tell you the truth, explain what happened and what the options are, and work with you to correct it."),
 ("Where is your office?","Our office is at 710 E McGlincy Ln, Ste 109, Campbell, CA 95008."),
 ("What kinds of clients do you work best with?","Honest, engaged clients who value workmanship and want to be informed throughout the project."),
]
VALUES=[("Trust","We want every client to look at our name and feel confident that things will be done right, and that we will be there if something needs fixing."),
 ("Accountability","Changes and decisions are documented in writing so expectations are clear for everyone."),
 ("Honesty","We would rather admit a mistake and correct it than lose a client's trust."),
 ("Responsiveness","When a question comes up, Roberto or Paula answers it. One of us is always there."),
 ("Attention to detail","The small details are what clients notice, so they are what we watch most closely.")]

def page_about():
    s=head("About REF Builders | Roberto & Paula, Campbell, CA","REF Builders is led by Roberto Flamenco and Paula: 25+ years of construction experience, careful finishes and honest communication.","about")
    s+=header("About")
    s+=phero("About REF Builders: Roberto, Paula & Our Team","A residential and commercial general contractor in Campbell, built on honest communication and careful finishes.","int-stair",[("About",None)])
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="story-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("Our story")}<h2 id="story-h" data-split>More Than 25 Years in Construction</h2></div>
  <div><p class="lede rv">Roberto arrived in the United States at 17. After a few months in other work, he found his place in construction and has stayed there for more than 25 years.</p>
  <p class="rv">Today he leads REF Builders with Paula. Together they build new homes, remodel and expand existing ones, and take on commercial and fire reconstruction work across the Bay Area. Their goal is to grow into larger, higher-value projects for clients who want great workmanship and a builder they can trust.</p>
  <p class="rv">Many clients come to us after a difficult experience elsewhere: unfinished work, missed inspections or promises that were not kept. We built our company on the opposite approach. We tell the truth, keep clients informed and stay until the job is done right.</p></div>
</div></section>

<section class="sec sec--stone" aria-labelledby="appr-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Our approach")}<h2 id="appr-h" data-split>From Rough to Finish, Covered by One Team</h2></div><p class="lede rv">Every project has two halves. Roberto and Paula each own one, and work side by side on both.</p></div>
  <div class="g2" style="align-items:stretch">
    <div class="img ar-43 wipe">{img("drone-oblique")}</div>
    <div class="img ar-43 wipe" style="transition-delay:.2s">{img("int-kitchen")}</div>
  </div>
  <div class="duo">
    <div class="duo__c rv"><span class="tag">The rough</span><h3>Structure, led by Roberto</h3><p class="muted">Foundations, framing and coordination with engineers. Roberto also offers practical input during engineering when a detail can be built more simply.</p></div>
    <div class="duo__c rv" style="--d:1"><span class="tag">The finish</span><h3>Finishes, led by Paula</h3><p class="muted">Paula picks up after insulation and drywall, coordinating floors, cabinetry, tile, fixtures and every detail that makes the home feel complete.</p></div>
  </div>
</div></section>

<section class="sec" aria-labelledby="ppl-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("People and leadership")}<h2 id="ppl-h" data-split>The People Behind REF Builders</h2></div><p class="lede rv">A couple, a team and the people you will speak with from the first meeting to the final walkthrough.</p></div>
  <div class="people">
    <article class="person rv"><div class="person__mono" aria-hidden="true">RF</div><h3>Roberto Flamenco</h3><span class="tag">Owner</span><p class="muted">Roberto has more than 25 years of personal construction experience. He leads foundations, framing and engineering coordination, and he is on site making sure the structure is right for every finish that follows.</p></article>
    <article class="person rv" style="--d:1"><div class="person__mono" aria-hidden="true">P</div><h3>Paula</h3><span class="tag">Finishes and client coordination</span><p class="muted">Paula coordinates the finishes and the client experience. She keeps selections on schedule, watches the small details and makes sure clients always know what is happening.</p></article>
  </div>
</div></section>

{strip("Talk with Roberto and Paula about your project.", "int-kitchen")}
<section class="sec sec--dark" aria-labelledby="val-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Values")}<h2 id="val-h" data-split>What We Stand For</h2></div><p class="lede rv">Values only matter when they show up in the work. Here is how ours do.</p></div>
  <ul class="why">{"".join(f'<li class="rv"><span class="n">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i,(t,d) in enumerate(VALUES))}</ul>
</div></section>

<section class="sec" aria-labelledby="exp-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Expertise")}<h2 id="exp-h" data-split>Where We Put Our Experience to Work</h2></div><div><p class="lede rv">Eight services across residential and commercial construction.</p><div class="rv" style="margin-top:20px">{link("All services","services.html")}</div></div></div>
  {svc_cards()}
  <div class="cta-strip rv" style="margin-top:clamp(60px,7vw,100px)"><h2>Want to see if we are the right fit for your project?</h2>{btn("Start Your Project")}</div>
</div></section>

{faq_block(ABOUT_FAQ, h2="Questions About REF Builders", stone=True)}
</main>'''
    s+=footer(True,"Let's Build Something You Can Trust")
    write("about.html", s)

SVCS_FAQ=[
 ("Which services does REF Builders offer?","Full home remodeling, new home construction, kitchen remodeling, bathroom remodeling, home additions, ADU construction, commercial construction and tenant improvements, and fire restoration and reconstruction."),
 ("How do I know which service fits my project?","Tell us what you want to achieve. Many projects combine services, such as an addition with a kitchen remodel, and we will help you define the scope."),
 ("Can you combine several services in one project?","Yes. We regularly coordinate combined projects, such as a full remodel with an addition or an ADU built alongside a main house remodel."),
 ("Do you work on both homes and commercial properties?","Yes. We work on residential projects and on commercial construction, tenant improvements and fire reconstruction."),
 ("Do you provide design services?","Design and plans are prepared by architectural and engineering partners. We help you connect with them and support the process."),
 ("Do you handle framing, plumbing and drywall?","These capabilities support our construction and remodeling services, including framing, foundations, drywall, plumbing, insulation coordination and finish coordination."),
 ("Do you work as a subcontractor?","Yes. In addition to general contracting, we work as a subcontractor where applicable."),
 ("When do you sign a construction agreement?","After your plans are approved, so the agreement reflects the approved design."),
 ("Do all services include warranty support?","Covered warranty items are handled under the terms in each client's agreement."),
 ("Which areas do your services cover?","Santa Clara County, San Mateo County, Alameda County and San Francisco."),
]
PROJ_FIT=[("Homeowners planning larger projects","Whole-home remodels, new homes and additions where finish quality matters."),("Property owners adding space","ADUs and additions that add living space to an existing property."),("Businesses and building owners","Tenant improvements and new commercial construction."),("Owners rebuilding after a fire","Residential and commercial reconstruction from structure to finish.")]

def page_services():
    s=head("Construction & Remodeling Services | REF Builders","Remodeling, new homes, additions, ADUs, commercial TI and fire reconstruction across Santa Clara, San Mateo and Alameda counties.","services")
    s+=header("Services")
    s+=phero("Residential & Commercial Construction Services","Eight services, one standard: honest communication, coordinated phases and careful finishes from rough work to completion.","int-open-plan",[("Services",None)])
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="wp-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("What we provide")}<h2 id="wp-h" data-split>One Builder for the Whole Project</h2></div>
  <div><p class="lede rv">REF Builders is a general contractor for homeowners, property owners and businesses across the Bay Area.</p><p class="rv">We build and remodel homes, add new living space, and take on commercial and fire reconstruction work. Framing, foundations, drywall, plumbing, insulation coordination and finish coordination support each service, and our architectural and engineering partners help prepare plans when you need them.</p></div>
</div></section>
<section class="sec sec--stone" aria-labelledby="sv-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Services")}<h2 id="sv-h" data-split>Choose Your Service</h2></div><p class="lede rv">Each service has its own page with scope, process and answers to common questions.</p></div>
  {svc_cards()}
</div></section>
{steps_cards(SERVICE_STEPS, h2="How we work. <em>On every service.</em>", lede="The same clear sequence applies whether you are remodeling a bathroom or building a new home.")}
{strip("Not sure which service fits? Tell us what you are planning.", "int-open-plan")}
<section class="sec sec--dark" aria-labelledby="fit-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Project fit")}<h2 id="fit-h" data-split>Who We Build For</h2></div><p class="lede rv">We do our best work with clients who value workmanship, honest communication and a clear process.</p></div>
  <ul class="why">{"".join(f'<li class="rv"><span class="n">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></li>' for i,(t,d) in enumerate(PROJ_FIT))}</ul>
</div></section>
{faq_block(SVCS_FAQ, h2="Questions About Our Services")}
</main>'''
    s+=footer(True,"Tell Us About Your Project")
    write("services.html", s)

def page_service(sv):
    others=[x for x in SERVICES if x["slug"]!=sv["slug"]]
    s=head(sv["title"], sv["desc"], sv["slug"])
    s+=header("Services")
    s+=phero(sv["h1"], sv["sub"], sv["img"], [("Services","services.html"),(sv["name"],None)])
    scope="".join(f'<div class="rv" style="--d:{i%3}"><span class="ic">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(t,d) in enumerate(sv["scope"]))
    steps="".join(f'<div class="step"><span class="step__dot">{i+1:02d}</span><span class="tag">Step {i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(t,d) in enumerate(SERVICE_STEPS))
    cities="".join(f'<a class="chip" href="{c["slug"]}.html">{c["name"]}</a>' for c in CITIES)
    proof_p = PROJECTS[0] if sv["slug"] in ("new-home-construction","home-additions","full-home-remodeling","accessory-dwelling-unit-construction") else PROJECTS[1]
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="ov-h"><div class="wrap g2">
  <div>{eyebrow("Service overview")}<h2 id="ov-h" data-split>{E(sv["name"])}, Done Properly</h2>{"".join(f'<p class="rv{" lede" if i==0 else ""}">{E(p)}</p>' for i,p in enumerate(sv["overview"]))}<div class="rv">{link("See all services","services.html")}</div></div>
  <div class="img ar-45 wipe">{img(sv["img2"], para=True)}</div>
</div></section>
<section class="sec sec--stone" aria-labelledby="sc-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Scope")}<h2 id="sc-h" data-split>What This Service Covers</h2></div><p class="lede rv">The exact scope follows your approved plans and agreement. These are the parts we typically coordinate.</p></div>
  <div class="scope">{scope}</div>
</div></section>
<section class="sec" aria-labelledby="pr-h"><div class="wrap proc">
  <div class="proc__stick">{eyebrow("Process")}<h2 id="pr-h" data-split>How Your Project Moves Forward</h2><p class="lede rv">You know what is happening, when it is happening and what we need from you.</p></div>
  <div class="steps"><div class="steps__rail"><div class="steps__fill"></div></div>{steps}</div>
</div></section>
{strip(f'Plan your {sv["name"].lower()} project with Roberto and Paula.', sv["img"])}
<section class="sec sec--dark" aria-labelledby="wy-h"><div class="wrap g2">
  <div>{eyebrow("Why REF Builders")}<h2 id="wy-h" data-split>Why Clients Choose Us for {E(sv["name"])}</h2><ul class="checks rv">{"".join(f"<li>{E(w)}</li>" for w in sv["why"])}</ul></div>
  <div><div class="county rv" style="border-top:1px solid var(--line-light)"><h2 style="font-size:22px;margin:0 0 14px">Coverage</h2><p style="font-size:15px">We provide {E(sv["name"].lower())} across Santa Clara County, San Mateo County, Alameda County and San Francisco.</p><div class="chips">{cities}</div><div style="margin-top:22px">{link("All service areas","service-areas.html")}</div></div></div>
</div></section>
<section class="sec" aria-labelledby="pp-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Project proof")}<h2 id="pp-h" data-split>Recent Work</h2></div><p class="lede rv">See how we carry structure and finishes through on a completed project.</p></div>
  <a class="pcard" href="{proof_p["slug"]}.html" style="display:block;max-width:none"><div class="pcard__img" style="aspect-ratio:21/9">{img(proof_p["img"], sizes="100vw")}</div><div class="pcard__b"><div><span class="tag">{E(proof_p["type"])}</span><h3>{E(proof_p["name"])}</h3></div><span class="btn btn--light" aria-hidden="true">View Project<span class="ar">{I["up"]}</span></span></div></a>
  <h2 class="rv" style="font-size:22px;margin:56px 0 18px">Related services</h2>
  <div class="related">{"".join(f'<a class="rlink rv" href="{o["slug"]}.html">{E(o["name"])}{I["ar"]}</a>' for o in others[:6])}</div>
</div></section>
{faq_block(sv["faqs"], h2=f'{sv["name"]} FAQs', stone=True)}
</main>'''
    s+=footer(True, f'Plan Your {sv["name"].replace("Accessory Dwelling Unit Construction","ADU").replace(" & Tenant Improvements"," Project").replace(" & Reconstruction"," Rebuild")} With REF Builders')
    write(sv["slug"]+".html", s)

def page_projects():
    s=head("Construction & Remodeling Projects | REF Builders","Browse REF Builders projects: new home construction, kitchens and interior finishes in the Bay Area.","projects")
    s+=header("Projects")
    s+=phero("Our Construction & Remodeling Projects","Real work, real photos. Explore how we carry each project from structure to the final finish.","drone-rear",[("Projects",None)])
    cards="".join(f'''<article class="pcard rv" style="flex:none;--d:{i}"><a href="{p["slug"]}.html" class="card__cover" aria-label="View project: {E(p["name"])}"></a><div class="pcard__img">{img(p["img"], sizes="(max-width:960px) 100vw, 50vw")}</div><div class="pcard__b"><div><span class="tag">{E(p["type"])} · {E(p["city"])}</span><h3>{E(p["name"])}</h3><p style="margin:10px 0 0;color:rgba(255,255,255,.75);font-size:15px;max-width:44ch">{E(p["intro"])}</p></div><span class="btn btn--light" aria-hidden="true">View Project<span class="ar">{I["up"]}</span></span></div></article>''' for i,p in enumerate(PROJECTS))
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="pi-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("Our work")}<h2 id="pi-h" data-split>Built to Be Looked at Closely</h2></div>
  <div><p class="lede rv">We show prospective clients our current work, photos and videos so they can judge our construction and finishes for themselves. This portfolio grows as projects and client stories are completed.</p></div>
</div></section>
<section class="sec sec--stone" style="padding-top:0;background:linear-gradient(var(--paper) 30%,var(--stone) 30%)" aria-labelledby="pg-h"><div class="wrap">
  <h2 id="pg-h" class="rv" style="font-size:clamp(26px,2.4vw,34px)">Project Gallery</h2>
  <div class="g2" style="gap:24px;align-items:stretch">{cards}</div>
</div></section>
{strip("Planning a similar project? Talk with Roberto and Paula.", "drone-front")}
<section class="sec" aria-labelledby="rs-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Related services")}<h2 id="rs-h" data-split>The Services Behind This Work</h2></div></div>
  {svc_cards(["new-home-construction","kitchen-remodeling","bathroom-remodeling","full-home-remodeling"])}
</div></section>
</main>'''
    s+=footer(True,"Planning a Similar Project?")
    write("projects.html", s)

def page_project(p):
    other=[x for x in PROJECTS if x["slug"]!=p["slug"]]
    s=head(p["title"], p["desc"], p["slug"])
    s+=header("Projects")
    s+=phero(p["h1"], p["intro"], p["img"], [("Projects","projects.html"),(p["name"],None)], cta=False)
    scope="".join(f'<div class="rv" style="--d:{i%3}"><span class="ic">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(t,d) in enumerate(p["scope"]))
    gal="".join(f'<figure class="rv"><div class="img {"ar-169" if (i%6) in (0,5) else "ar-43"} wipe">{img(g)}</div></figure>' for i,g in enumerate(p["gallery"]))
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="po-h"><div class="wrap">
  {eyebrow("Project overview")}<h2 id="po-h" data-split>Project Overview</h2>
  <div class="facts rv"><div><span class="tag">Location</span><b>{E(p["city"])}</b></div><div><span class="tag">Project type</span><b>{E(p["type"])}</b></div><div><span class="tag">Role</span><b>General contractor</b></div><div><span class="tag">Delivery</span><b>Structure to finish</b></div></div>
</div></section>
<section class="sec sec--stone" aria-labelledby="sw-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Scope of work")}<h2 id="sw-h" data-split>Scope of Work</h2></div></div>
  <div class="scope" style="grid-template-columns:repeat(2,minmax(0,1fr))">{scope}</div>
</div></section>
<section class="sec" aria-labelledby="ca-h"><div class="wrap g2">
  <div>{eyebrow("Challenge and approach")}<h2 id="ca-h" data-split>Challenge and Approach</h2><p class="lede rv">{E(p["challenge"])}</p></div>
  <div class="img ar-43 wipe">{img(p["gallery"][1])}</div>
</div></section>
{strip("Want results like these? Tell us about your project.", p["img"])}
<section class="sec sec--dark" aria-labelledby="dr-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("Delivery")}<h2 id="dr-h" data-split>Delivery and Results</h2></div><p class="lede rv">{E(p["result"])}</p>
</div></section>
<section class="sec" aria-labelledby="gl-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Gallery")}<h2 id="gl-h" data-split>Project Gallery</h2></div></div>
  <div class="gallery">{gal}</div>
</div></section>
<section class="sec sec--stone" aria-labelledby="mp-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("More projects")}<h2 id="mp-h" data-split>More Projects</h2></div><div class="rv">{link("All projects","projects.html")}</div></div>
  <div class="g2" style="gap:24px">{"".join(f'<article class="card rv"><div class="card__img">{img(o["img"])}</div><div class="card__b"><span class="card__n">{E(o["type"])}</span><h3>{E(o["name"])}</h3><p>{E(o["intro"])}</p><a class="link-ar" href="{o["slug"]}.html">View Project{I["ar"]}</a></div></article>' for o in other)}
  <div class="rv"><h3 style="font-size:20px">Related services</h3><div class="related" style="grid-template-columns:1fr">{"".join(f'<a class="rlink" href="{r}.html">{E(SVC[r]["name"])}{I["ar"]}</a>' for r in p["related"])}<a class="rlink" href="service-areas.html">Service Areas{I["ar"]}</a></div></div></div>
</div></section>
</main>'''
    s+=footer(True,"Want Results Like These?")
    write(p["slug"]+".html", s)

AREAS_FAQ=[
 ("Which areas does REF Builders serve?","Santa Clara County, San Mateo County, Alameda County and San Francisco."),
 ("Which cities have dedicated service area pages?","Palo Alto, Stanford, Redwood City, Saratoga and Los Gatos each have their own page."),
 ("Do you work outside the cities listed?","Our coverage includes the four counties and regions listed. Named areas also include Hillsborough, San Jose, Fremont and San Francisco. Contact us to confirm your location."),
 ("Where is your office?","Our office is at 710 E McGlincy Ln, Ste 109, Campbell, CA 95008."),
 ("Do you have offices in every city you serve?","No. We work from our Campbell office and travel to projects across our service area."),
 ("Are all services available in every area?","Our services are available across our coverage area. Tell us your location and project type and we will confirm."),
 ("Do you work in San Francisco?","Yes. San Francisco is part of our service area."),
 ("Do you serve the East Bay?","Yes. Alameda County, including Fremont, is part of our coverage."),
 ("Do you take commercial projects in all areas?","Commercial construction and tenant improvements are available across our service area. Contact us with your project location."),
 ("How do I confirm you can take my project?","Send your project city and type through the form or call (831) 566-9040."),
]

def page_areas():
    s=head("Service Areas | REF Builders","REF Builders serves Santa Clara County, San Mateo County, Alameda County and San Francisco from our office in Campbell, CA.","service-areas")
    s+=header("Service Areas")
    s+=phero("Service Areas Across the Bay Area","From our office in Campbell, we build and remodel across four Bay Area counties and regions.","drone-oblique",[("Service Areas",None)])
    groups=""
    for name, slugs, others in COUNTIES:
        cards="".join(f'<a class="rlink" href="{x}.html">{CTY[x]["name"]}{I["ar"]}</a>' for x in slugs)
        oth=", ".join(others)
        groups+=f'<div class="county rv" style="border-color:var(--line)"><h3>{E(name)}</h3>{("<div class=%srelated%s style=%sgrid-template-columns:repeat(2,minmax(0,1fr))%s>"%(chr(34),chr(34),chr(34),chr(34)))+cards+"</div>" if cards else ""}<p class="muted" style="margin:{"14px" if cards else "0"} 0 0;font-size:15px">{("Also serving: "+E(oth)) if oth!=name else "Citywide service across San Francisco"}</p></div>'
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="co-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("Coverage overview")}<h2 id="co-h" data-split>Where We Build</h2></div>
  <div><p class="lede rv">REF Builders serves Santa Clara County, San Mateo County, Alameda County and San Francisco.</p><p class="rv">Our office is in Campbell, and we travel to projects across the South Bay, the Peninsula, the East Bay and San Francisco. We do not have offices in each city we serve. If your property is near one of these areas, contact us to confirm.</p></div>
</div></section>
<section class="sec sec--dark" aria-labelledby="rg-h"><div class="wrap areas">
  {county_map()}
  <div>{eyebrow("Regions")}<h2 id="rg-h" data-split>Counties and Cities</h2>{county_list()}</div>
</div></section>
<section class="sec" aria-labelledby="cg-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("City pages")}<h2 id="cg-h" data-split>Find Your Community</h2></div><p class="lede rv">Each community page covers the projects we build there and answers local questions.</p></div>
  <div style="display:grid;gap:0;border-top:1px solid var(--line)">{groups}</div>
</div></section>
{strip("Not sure if we cover your area? Send us your project city.", "drone-oblique")}
<section class="sec sec--stone" aria-labelledby="sa-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Services available")}<h2 id="sa-h" data-split>Services Across Our Coverage Area</h2></div><div class="rv">{link("All services","services.html")}</div></div>
  {svc_cards()}
</div></section>
<section class="sec" aria-labelledby="rp-h"><div class="wrap g2">
  <div class="img ar-43 wipe">{img("drone-front")}</div>
  <div>{eyebrow("Regional proof")}<h2 id="rp-h" data-split>Work You Can Look Up Close</h2><p class="lede rv">We introduce prospective clients to current projects, photos and videos from around the Bay Area so you can see our structure and finishes before you decide.</p><div class="rv">{link("View projects","projects.html")}</div></div>
</div></section>
{faq_block(AREAS_FAQ, h2="Service Area Questions", stone=True)}
</main>'''
    s+=footer(True,"Confirm Your Project Location")
    write("service-areas.html", s)

def page_city(c):
    s=head(c["title"], c["desc"], c["slug"])
    s+=header("Service Areas")
    s+=phero(c["h1"], c["sub"], c["img"], [("Service Areas","service-areas.html"),(c["name"],None)])
    cards=svc_cards(c["services"], cols=3, numbered=False)
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="li-h"><div class="wrap g2 g2--top">
  <div>{eyebrow(c["county"])}<h2 id="li-h" data-split>Building in {E(c["name"])}</h2></div>
  <div>{"".join(f'<p class="rv{" lede" if i==0 else ""}">{E(p)}</p>' for i,p in enumerate(c["intro"]))}<div class="rv">{link(f'Back to all service areas','service-areas.html')}</div></div>
</div></section>
<section class="sec sec--stone" aria-labelledby="ls-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Services available")}<h2 id="ls-h" data-split>Services in {E(c["name"])}</h2></div><div class="rv">{link("All services","services.html")}</div></div>
  {cards}
</div></section>
<section class="sec" aria-labelledby="ap-h"><div class="wrap g2">
  <div class="img ar-45 wipe">{img(c["img"] if c["img"]!="ext-patio" else "ext-yard", para=True)}</div>
  <div>{eyebrow("Approach")}<h2 id="ap-h" data-split>How We Work in {E(c["name"])}</h2><p class="lede rv">{E(c["approach"])}</p><ul class="checks rv"><li>Phase dates shared before each stage</li><li>Selection deadlines tied to rough work</li><li>Changes documented in writing</li><li>Direct access to Roberto and Paula</li></ul></div>
</div></section>
{strip(f'Planning a project in {c["name"]}? Talk with Roberto and Paula.', c["img"])}
<section class="sec sec--dark" aria-labelledby="lp-h"><div class="wrap g2">
  <div>{eyebrow("Local coverage")}<h2 id="lp-h" data-split>Close to {E(c["name"])}</h2><p class="lede rv">{E(c["name"])} is part of our {E(c["county"])} coverage, served from our office at {BIZ["addr1"]} in Campbell. We do not have an office in {E(c["name"])}; we travel to each project.</p><div class="rv" style="margin-top:28px">{link("See our projects","projects.html")}</div></div>
  {county_map()}
</div></section>
{faq_block(c["faqs"], h2=f'{c["name"]} Project Questions', eyebrow_t="Local FAQs", stone=True)}
</main>'''
    s+=footer(True,f'Start Your {c["name"]} Project')
    write(c["slug"]+".html", s)

CONTACT_FAQ=[
 ("What is the best way to reach REF Builders?","Call (831) 566-9040, email refbuilders@gmail.com or send the inquiry form on this page."),
 ("What information should I include in my inquiry?","Your project city, the type of project, whether you have plans and your ideal timing. Photos are helpful too."),
 ("Do I need plans before contacting you?","No. If you do not have plans yet, we can introduce you to architect and engineering partners."),
 ("Can I meet you at your office?","Yes. We meet clients at our Campbell office at 710 E McGlincy Ln, Ste 109."),
 ("What happens after I submit the form?","We review your details and reach out to talk about your project and arrange next steps."),
 ("Can I see examples of your work?","Yes. We share current projects, photos and videos during the first conversations."),
 ("Do you take small projects?","Tell us about your project. We focus on remodels, additions, new homes, ADUs, commercial and fire reconstruction work."),
 ("Do you work with commercial clients?","Yes. We take commercial construction and tenant improvement projects."),
 ("Which areas do you cover?","Santa Clara County, San Mateo County, Alameda County and San Francisco."),
 ("Will you send me text messages?","Only if you consent using the boxes on the form. You can reply STOP at any time to opt out."),
]

def page_contact():
    s=head("Contact REF Builders | Start Your Project","Contact REF Builders in Campbell, CA to discuss a remodel, new home, addition, ADU, commercial or fire reconstruction project.","contact")
    s+=header("Contact")
    s+=phero("Contact REF Builders About Your Project","Tell us what you are planning. We will review your details and reach out to talk about next steps.","ext-patio",[("Contact",None)])
    whatsend=[("Project location","The city or neighborhood where the work will happen."),("Project type","Remodel, new home, addition, ADU, commercial or fire reconstruction."),("Plans and photos","Any plans, drawings or photos you already have."),("Timing","When you would like to begin and any important dates.")]
    nxt=[("We review your inquiry","We read your details and note any questions."),("We reach out","We contact you to talk through your project and goals."),("We meet","We meet at our Campbell office or discuss next steps and show you our work.")]
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="ci-h"><div class="wrap g2 g2--top">
  <div>{eyebrow("Contact information")}<h2 id="ci-h" data-split>Talk With Roberto and Paula</h2><p class="lede rv">Call, email or send the form. We are glad to answer questions before you commit to anything.</p>
    <div class="contact-cards rv">
      <a class="ccard" href="tel:{BIZ["tel"]}"><span class="ic">{I["phone"]}</span><span><h3>Business phone</h3><b>{BIZ["phone"]}</b></span></a>
      <a class="ccard" href="tel:{BIZ["owner_tel"]}"><span class="ic">{I["phone"]}</span><span><h3>Owner contact</h3><b>{BIZ["owner_phone"]}</b></span></a>
      <a class="ccard" href="mailto:{BIZ["email"]}"><span class="ic">{I["mail"]}</span><span><h3>Email</h3><b>{BIZ["email"]}</b></span></a>
      <div class="ccard"><span class="ic">{I["pin"]}</span><span><h3>Office</h3><b>{BIZ["addr1"]}, {BIZ["addr2"]}</b></span></div>
    </div>
  </div>
  <div>{eyebrow("What to send")}<h2 data-split style="font-size:clamp(28px,2.8vw,40px)">What Helps Us Respond</h2><ul class="checks rv">{"".join(f"<li><span><b style='color:var(--ink)'>{E(t)}.</b> {E(d)}</span></li>" for t,d in whatsend)}</ul></div>
</div></section>
<section class="sec sec--stone" aria-labelledby="fm-h" id="form-section"><div class="wrap g2 g2--top">
  <div>{eyebrow("Inquiry form")}<h2 id="fm-h" data-split>Send Us Your Project Details</h2><p class="lede rv">Fields marked * are required. Both text message consent boxes must be selected to submit.</p></div>
  <div class="rv form-card" style="scroll-margin-top:120px" id="form-wrap">{form("form", dark=False)}</div>
</div></section>
<section class="sec" aria-labelledby="wn-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("What happens next")}<h2 id="wn-h" data-split>What Happens Next</h2></div></div>
  <div class="scope">{"".join(f'<div class="rv" style="--d:{i}"><span class="ic">{i+1:02d}</span><h3>{E(t)}</h3><p>{E(d)}</p></div>' for i,(t,d) in enumerate(nxt))}</div>
</div></section>
<section class="sec sec--dark" aria-labelledby="ca2-h"><div class="wrap areas">
  <div>{eyebrow("Service areas")}<h2 id="ca2-h" data-split>Where We Work</h2>{county_list()}<div class="rv" style="margin-top:28px">{link("All service areas","service-areas.html")}</div></div>
  {county_map()}
</div></section>
{faq_block(CONTACT_FAQ, h2="Questions Before You Reach Out", stone=True)}
</main>'''
    s+=footer(False)
    s=s.replace('id="form" novalidate','id="form" novalidate style="scroll-margin-top:110px"')
    write("contact.html", s)

FAQ_PAGE=[
 ("Services",[
  ("What services does REF Builders offer?","Full home remodeling, new home construction, kitchen remodeling, bathroom remodeling, home additions, ADU construction, commercial construction and tenant improvements, and fire restoration and reconstruction."),
  ("Do you build new homes from the ground up?","Yes. We build new homes from foundation and framing through finishes, based on approved plans."),
  ("Do you build ADUs?","Yes. We build accessory dwelling units, coordinating with your design team."),
  ("Do you take commercial projects?","Yes. We take commercial construction and tenant improvements, as a general contractor or, where applicable, as a subcontractor."),
  ("Do you rebuild after fires?","Yes. We handle construction and rebuilding following fire damage for homes and commercial properties.")]),
 ("Process",[
  ("Do I need plans before I contact you?","No. We can introduce you to architect and engineering partners and support the design process."),
  ("When do you sign the construction agreement?","After your plans are approved, so the agreement reflects the final design."),
  ("How will I know what is happening during construction?","We explain each phase before it starts, with expected dates and the selections that are due."),
  ("When do I need to choose fixtures and finishes?","Some are needed early. Bathroom valves and kitchen layouts are required during rough plumbing. We give you deadlines for each phase."),
  ("How are changes handled?","Changes are discussed, explained and documented in writing before the work is done.")]),
 ("Our Team",[
  ("Who leads REF Builders?","Roberto Flamenco, the owner, and Paula. Roberto leads rough construction and Paula coordinates finishes."),
  ("How much experience does Roberto have?","More than 25 years of personal construction experience."),
  ("Do you work with architects and engineers?","Yes. Our partners prepare designs and plans, and we guide you through those relationships and the construction."),
  ("What if something goes wrong?","We tell you the truth, explain the options and work with you to correct it."),
  ("Do you provide warranty support?","Yes. Covered warranty issues are handled under the terms in your agreement.")]),
 ("Coverage and Getting Started",[
  ("Which areas do you serve?","Santa Clara County, San Mateo County, Alameda County and San Francisco."),
  ("Which cities do you serve most?","Palo Alto, Stanford, Redwood City, Saratoga and Los Gatos, along with Hillsborough, San Jose, Fremont and San Francisco."),
  ("Where is your office?","710 E McGlincy Ln, Ste 109, Campbell, CA 95008."),
  ("How do I start a project?","Call (831) 566-9040 or send the inquiry form with your project city, type and any plans."),
  ("Can I see your work first?","Yes. We share current projects, photos and videos with prospective clients.")]),
]

def page_faqs():
    s=head("Frequently Asked Questions | REF Builders","Answers about REF Builders services, process, team, coverage and how to start a remodel, new home, addition or ADU.","faqs")
    s+=header("About")
    s+=phero("Frequently Asked Questions","Answers about our services, process, team and coverage. Still have a question? Call us or send a message.","int-great-room",[("About","about.html"),("FAQs",None)], cta=False)
    groups=""
    for gname, items in FAQ_PAGE:
        it="".join(f'''<div class="acc__i"><h3 class="acc__h"><button class="acc__q" aria-expanded="false"><span>{E(q)}</span><span class="acc__ic" aria-hidden="true"></span></button></h3><div class="acc__a"><div><p>{E(a)}</p></div></div></div>''' for q,a in items)
        groups+=f'<div class="faq-group rv"><h2>{E(gname)}</h2><div class="acc">{it}</div></div>'
    s+=f'''<main id="main">
<section class="sec"><div class="wrap faq">
  <div class="faq__side">{eyebrow("FAQs")}<p class="lede rv">Questions are grouped by topic. Each answer reflects how we actually work.</p><div class="chips rv" style="margin-top:20px">{"".join(f'<a class="chip" href="{x}">{n}</a>' for n,x in [("Services","services.html"),("Service Areas","service-areas.html"),("Projects","projects.html"),("Contact","contact.html")])}</div></div>
  <div>{groups}</div>
</div></section>
</main>'''
    s+=footer(True,"Still Have Questions? Let's Talk")
    write("faqs.html", s)

def page_blog():
    s=head("Blogs | REF Builders","Planning guides from REF Builders for Bay Area homeowners: remodel selections, design teams, and building new homes, additions and ADUs.","blog")
    s+=header("About")
    s+=phero("Blogs","Practical planning guides for homeowners getting ready to remodel, add on or build.","int-kitchen-sink",[("About","about.html"),("Blogs",None)], cta=False)
    cards="".join(f'''<article class="bcard rv" style="--d:{i}"><a class="img wipe" href="{p["slug"]}.html" tabindex="-1" aria-hidden="true">{img(p["img"])}</a><div><span class="tag">{E(p["tag"])} · {E(p["read"])}</span><h3 style="margin-top:10px"><a href="{p["slug"]}.html">{E(p["h1"])}</a></h3><p class="muted" style="margin:10px 0 16px">{E(p["excerpt"])}</p>{link("Read More", p["slug"]+".html")}</div></article>''' for i,p in enumerate(POSTS))
    s+=f'''<main id="main">
<section class="sec" aria-labelledby="al-h"><div class="wrap">
  <div class="head-row"><div>{eyebrow("Article listing")}<h2 id="al-h" data-split>Latest Articles</h2></div><p class="lede rv">Guides based on how we plan and build projects every day.</p></div>
  <div class="bcards">{cards}</div>
</div></section>
</main>'''
    s+=footer(True,"Have a Project in Mind?")
    write("blog.html", s)

def page_post(p):
    other=[x for x in POSTS if x["slug"]!=p["slug"]]
    s=head(p["title_tag"]+" | REF Builders" if len(p["title_tag"])<=40 else p["title_tag"], p["desc"], p["slug"])
    s+=header("About")
    s+=phero(p["h1"], p["excerpt"], p["img"], [("Blogs","blog.html"),(p["h1"],None)], cta=False)
    body=""
    for h2, parts in p["sections"]:
        body+=f'<h2>{E(h2)}</h2>'
        for part in parts:
            if isinstance(part, list):
                body+="".join(f'<h3>{E(t)}</h3><p>{E(d)}</p>' for t,d in part)
            else:
                body+=f'<p>{E(part)}</p>'
    sv=SVC[p["service"]]; sv2=SVC[p["service2"]]
    s+=f'''<main id="main">
<article class="sec"><div class="wrap" style="display:grid;grid-template-columns:minmax(0,1fr);justify-items:center">
  <div class="prose">
    <p class="tag" style="margin-bottom:18px">{E(p["tag"])} · {E(p["read"])} · REF Builders</p>
    <p class="lede">{E(p["intro"])}</p>
    {body}
    <div class="callout">Planning a project? We give every client a list of selection deadlines tied to each phase.</div>
  </div>
</div></article>
{faq_block(p["faqs"], h2="Questions on This Topic", stone=True)}
<section class="sec" aria-labelledby="ns-h"><div class="wrap">
  <div class="cta-strip rv"><div><span class="eyebrow">Next step</span><h2 id="ns-h">Ready to plan your project?</h2><p class="muted" style="margin:10px 0 0">Learn more about <a class="link-ar" href="{sv["slug"]}.html">{E(sv["name"])}</a> and <a class="link-ar" href="{sv2["slug"]}.html">{E(sv2["name"])}</a>.</p></div>{btn("Start Your Project")}</div>
  <h2 class="rv" style="font-size:22px;margin:56px 0 18px">Related articles</h2>
  <div class="related">{"".join(f'<a class="rlink rv" href="{o["slug"]}.html">{E(o["h1"])}{I["ar"]}</a>' for o in other)}<a class="rlink rv" href="blog.html">All articles{I["ar"]}</a></div>
</div></section>
</main>'''
    s+=footer(True,"Talk to REF Builders")
    write(p["slug"]+".html", s)

def legal_page(kind):
    L=BIZ["legal"]; eff="November 25, 2026"
    if kind=="privacy":
        h1="Privacy Policy"; fn="privacy-policy.html"
        body=f'''<p><b>{L}</b><br>Effective Date: {eff}</p>
<p>{L} (“we,” “our,” or “us”) is committed to protecting your privacy. This Privacy Policy explains how we collect, use, protect, and manage your personal information when you visit our website, contact us, or use our services.</p>
<p>By using our website or submitting your information, you agree to the terms of this Privacy Policy.</p>
<h2>1. Personal Information We Collect</h2><p>We may collect the following types of personal data from users:</p><ul><li>Full name</li><li>Email address</li><li>Phone number</li><li>Physical address or project location</li><li>Service inquiry details or project information</li><li>IP address</li><li>Device and browser information</li><li>Website usage data (pages visited, time spent, interactions)</li><li>SMS communication preferences and consent status</li></ul>
<h2>2. How We Use Collected Data</h2><p>We use the information we collect for the following purposes:</p><ul><li>To respond to inquiries and provide quotes or estimates</li><li>To schedule appointments and communicate about projects</li><li>To deliver requested services</li><li>To improve our website and customer experience</li><li>To send service updates, reminders, and transactional messages</li><li>To send marketing or promotional communications (only with consent)</li><li>To comply with legal and regulatory requirements</li></ul>
<h2>3. SMS Consent: How It Is Obtained and Used</h2><p>By providing your phone number and opting in through our website forms, contact forms, or other communication channels, you consent to receive SMS messages from {L}.</p><p>SMS consent is obtained when:</p><ul><li>You check a consent box on a web form</li><li>You submit your phone number for service inquiries</li><li>You verbally agree to receive SMS communications</li><li>You opt in through a text message confirmation process</li></ul><p>SMS messages may include:</p><ul><li>Appointment confirmations and reminders</li><li>Project updates</li><li>Customer service communications</li><li>Promotional or marketing messages (if opted in)</li></ul><p>Message frequency: daily. You may opt out of SMS messages at any time by replying STOP to any message. Message and data rates may apply.</p>
<h2>4. Cookies and Tracking Technologies</h2><p>We use cookies and similar tracking technologies to enhance user experience and analyze website performance. These may include:</p><ul><li>Session cookies</li><li>Analytics cookies (such as Google Analytics)</li><li>Advertising or remarketing pixels</li><li>Website performance and traffic monitoring tools</li></ul><p>These technologies help us understand how users interact with our website and improve our services. You can manage or disable cookies through your browser settings.</p>
<h2>5. How We Protect Your Data</h2><p>We implement reasonable administrative, technical, and physical security measures to protect your personal information, including:</p><ul><li>Secure servers and hosting environments</li><li>Encryption where appropriate</li><li>Limited access to personal data</li><li>Internal policies to protect against unauthorized access, disclosure, or misuse</li></ul><p>While no system is 100% secure, we take appropriate steps to safeguard your information.</p>
<h2>6. Accessing or Deleting Your Data</h2><p>You have the right to:</p><ul><li>Request access to the personal data we hold about you</li><li>Request corrections to inaccurate information</li><li>Request deletion of your personal data</li></ul><p>To make a request, please contact us using the information below. We will respond within a reasonable timeframe in accordance with applicable laws.</p>
<h2>7. Phone Number Sharing or Selling</h2><p>We do NOT sell, rent, or share your phone number or personal information with any third parties for marketing or promotional purposes.</p><p>Your phone number is used solely for communication between you and {L}. Text messaging originator opt-in data and consent will not be shared with any third parties under any circumstances.</p><p>No mobile information will be shared with third parties or affiliates for marketing or promotional purposes. Information sharing to subcontractors in support services, such as customer service, is permitted. All other use case categories exclude text messaging originator opt-in data and consent; this information will not be shared with any third parties.</p>
<h2>8. Contact Information</h2><p>If you have any questions about this Privacy Policy or your personal data, please contact us:</p><p>{L}<br>Email: <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a><br>Phone: <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a><br>Address: {BIZ["addr1"]}, {BIZ["addr2"]}</p>'''
        desc="How REF Builders collects, uses and protects personal information and SMS consent submitted through this website."
    else:
        h1="Terms and Conditions"; fn="terms-and-conditions.html"
        body=f'''<p><b>{L}</b><br>Effective Date: {eff}</p>
<p>By providing your phone number and opting in to receive communications from {L} (“we,” “our,” or “us”), you agree to these Terms and Conditions related to SMS and electronic communications.</p>
<h2>1. Types of Messages You Will Receive</h2><p>By opting in, you may receive SMS, MMS, or other electronic messages from {L}, including but not limited to:</p><ul><li>Appointment confirmations and reminders</li><li>Project updates and scheduling notifications</li><li>Customer service and support communications</li><li>Estimates, invoices, and transactional messages</li><li>Promotional offers, discounts, and marketing messages (if you have opted in to receive marketing)</li></ul><p>Message frequency: daily.</p>
<h2>2. SMS Unsubscribe / Opt-Out Instructions</h2><p>You may unsubscribe from SMS messages from {L} at any time.</p><p>To opt out, simply reply STOP to any SMS message you receive from us.</p><p>After you send STOP, you will receive one final confirmation message confirming that you have been unsubscribed. You will no longer receive SMS messages unless you opt in again.</p><p>For help, you may reply HELP or contact us directly using the contact information below.</p><p>Message and data rates may apply.</p><p>If you have any questions about your text plan or data plan, it is best to contact your wireless provider.</p>
<h2>3. Carrier Disclaimer</h2><p>Mobile carriers are not liable for delayed or undelivered messages. {L} is not responsible for any messaging delays, failures, or errors caused by mobile carriers or service providers.</p>
<h2>4. Consent Not Required for Purchase</h2><p>Your consent to receive SMS messages is not required as a condition of purchasing any goods or services from {L}.</p>
<h2>5. Age Requirement</h2><p>By using this website and opting in to receive communications, you confirm that you are at least 18 years of age. {L} does not knowingly collect or communicate with individuals under the age of 18.</p>
<h2>6. Privacy Policy</h2><p>Your use of our website and communications is also governed by our Privacy Policy. Please review our Privacy Policy to understand how we collect, use, and protect your information:</p><p>Privacy Policy: <a href="privacy-policy.html">Privacy Policy</a></p>
<h2>7. Changes to These Terms</h2><p>{L} reserves the right to update or modify these Terms and Conditions at any time. Updates will be posted on this page with a revised effective date.</p>
<p>Contact: <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> | <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a></p>'''
        desc="Terms and conditions for SMS and electronic communications from REF Builders, including opt-out, frequency and consent details."
    s=head(f"{h1} | REF Builders", desc, fn.replace(".html",""))
    s+=header("", inner=True)
    s+=f'''<main id="main"><section class="phero phero--plain"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{h1}</span></nav><div class="phero__top"><h1 data-split>{h1}</h1></div></div></section>
<section class="sec"><div class="wrap"><div class="prose legal">{body}</div></div></section></main>'''
    s+=footer(True,"Questions? Contact REF Builders")
    write(fn, s)

if __name__=="__main__":
    page_home(); page_about(); page_services(); [page_service(x) for x in SERVICES]
    page_projects(); [page_project(x) for x in PROJECTS]; page_areas(); [page_city(x) for x in CITIES]
    page_contact(); page_faqs(); page_blog(); [page_post(x) for x in POSTS]
    legal_page("privacy"); legal_page("terms")
    print("built", len([f for f in os.listdir(OUT) if f.endswith(".html")]), "pages")
