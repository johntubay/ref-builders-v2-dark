/* REF Builders | site.js  (no dependencies) */
(function(){
  "use strict";
  var d=document, w=window, html=d.documentElement;
  var reduce=w.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* header: solid + shrink on scroll */
  var hdr=d.querySelector(".hdr");
  function onScroll(){ if(hdr) hdr.classList.toggle("is-solid", w.scrollY>40); }
  w.addEventListener("scroll", onScroll, {passive:true}); onScroll();

  /* desktop dropdowns: keyboard + touch support */
  d.querySelectorAll(".nav>ul>li.has-dd").forEach(function(li){
    var a=li.querySelector(".nav__a");
    a.addEventListener("keydown",function(e){
      if(e.key==="ArrowDown"||e.key===" "){e.preventDefault();li.classList.add("is-open");a.setAttribute("aria-expanded","true");var f=li.querySelector(".dd a");f&&f.focus();}
      if(e.key==="Escape"){li.classList.remove("is-open");a.setAttribute("aria-expanded","false");}
    });
    li.addEventListener("mouseenter",function(){a.setAttribute("aria-expanded","true")});
    li.addEventListener("mouseleave",function(){li.classList.remove("is-open");a.setAttribute("aria-expanded","false")});
    li.addEventListener("focusout",function(e){ if(!li.contains(e.relatedTarget)){li.classList.remove("is-open");a.setAttribute("aria-expanded","false");} });
    li.querySelector(".dd").addEventListener("keydown",function(e){
      var links=[].slice.call(li.querySelectorAll(".dd a")), i=links.indexOf(d.activeElement);
      if(e.key==="ArrowDown"){e.preventDefault();(links[i+1]||links[0]).focus();}
      if(e.key==="ArrowUp"){e.preventDefault();(links[i-1]||a).focus();}
      if(e.key==="Escape"){li.classList.remove("is-open");a.focus();}
    });
  });

  /* mobile menu */
  var burger=d.querySelector(".burger");
  if(burger){
    burger.addEventListener("click",function(){
      var open=d.body.classList.toggle("menu-open");
      burger.setAttribute("aria-expanded",open?"true":"false");
    });
    d.querySelectorAll(".mnav__tg").forEach(function(b){
      b.addEventListener("click",function(){var li=b.closest("li");var o=li.classList.toggle("is-open");b.setAttribute("aria-expanded",o?"true":"false");});
    });
    d.addEventListener("keydown",function(e){ if(e.key==="Escape"&&d.body.classList.contains("menu-open")){d.body.classList.remove("menu-open");burger.setAttribute("aria-expanded","false");burger.focus();} });
  }

  /* split headings into words for the mask reveal */
  d.querySelectorAll("[data-split]").forEach(function(el){
    var i=0;
    function walk(node){
      [].slice.call(node.childNodes).forEach(function(n){
        if(n.nodeType===3){
          var frag=d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function(t){
            if(!t) return;
            if(/^\s+$/.test(t)){frag.appendChild(d.createTextNode(t));return;}
            var o=d.createElement("span");o.className="w";
            var s=d.createElement("span");s.textContent=t;s.style.setProperty("--i",i++);
            o.appendChild(s);frag.appendChild(o);
          });
          n.parentNode.replaceChild(frag,n);
        } else if(n.nodeType===1 && n.tagName!=="BR"){ walk(n); }
      });
    }
    el.setAttribute("aria-label",el.textContent.replace(/\s+/g," ").trim());
    walk(el); el.classList.add("split");
    el.querySelectorAll(".w").forEach(function(x){x.setAttribute("aria-hidden","true")});
  });

  /* gradient heading accents: give every split word its slice of one gradient that runs
     across the whole phrase in reading order, even when the phrase wraps to a new line */
  function gradWords(){
    d.querySelectorAll("h1 em,h2 em").forEach(function(em){
      var ws=[].slice.call(em.querySelectorAll(".w")); if(!ws.length) return;
      var widths=ws.map(function(x){return x.getBoundingClientRect().width}), total=0, at=0;
      widths.forEach(function(v){total+=v});
      ws.forEach(function(x,i){
        var s=x.firstElementChild; if(!s) return;
        s.style.backgroundSize=total+"px 100%";
        s.style.backgroundPosition=(-at)+"px 0";
        at+=widths[i];
      });
    });
  }
  gradWords();
  if(d.fonts&&d.fonts.ready) d.fonts.ready.then(gradWords);
  var gwT; w.addEventListener("resize",function(){ clearTimeout(gwT); gwT=setTimeout(gradWords,120); });

  /* image loading: fade in when decoded, mark container ready */
  d.querySelectorAll(".img img,.card__img img,.pcard__img img,.phero__media img").forEach(function(im){
    var box=im.parentElement;
    function done(){ im.classList.add("loaded"); box.classList.add("ok"); }
    function fail(){ box.classList.add("ok"); im.classList.add("loaded"); }
    if(im.complete && im.naturalWidth){ done(); return; }
    im.classList.add("fade");
    im.addEventListener("load",function(){ (im.decode? im.decode():Promise.resolve()).then(done,done); });
    im.addEventListener("error",fail);
  });

  if("IntersectionObserver" in w){
    var pre=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ e.target.loading="eager"; pre.unobserve(e.target);} }); },{rootMargin:"150% 0px 150% 0px"});
    d.querySelectorAll('img[loading="lazy"]').forEach(function(i){pre.observe(i)});
  }

  /* reveal on scroll */
  /* step cards start fully masked (clip-path), which browsers count as 0% visible,
     so they get their own trigger that fires as soon as the card's box reaches the screen */
  var masked=d.querySelectorAll(".scard.rv,.xcard");
  var targets=[].filter.call(d.querySelectorAll(".rv,.split,.wipe,.roof-draw,[data-io]"),function(t){return !t.matches(".scard.rv")});
  if("IntersectionObserver" in w && !reduce){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); io.unobserve(e.target);} });
    },{rootMargin:"0px 0px -8% 0px",threshold:.12});
    targets.forEach(function(t){io.observe(t)});
    var mio=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add("in"); mio.unobserve(e.target);} });
    },{rootMargin:"0px 0px -12% 0px",threshold:0});
    masked.forEach(function(t){mio.observe(t)});
  } else { targets.forEach(function(t){t.classList.add("in")}); masked.forEach(function(t){t.classList.add("in")}); }

  /* gentle parallax (translate only, never scale) */
  var par=[].slice.call(d.querySelectorAll("[data-para]"));
  if(par.length && !reduce){
    var tick=false;
    function para(){
      par.forEach(function(el){
        var r=el.parentElement.getBoundingClientRect(), vh=w.innerHeight;
        if(r.bottom<0||r.top>vh) return;
        var p=(r.top+r.height/2-vh/2)/vh, k=parseFloat(el.dataset.para)||.08;
        el.style.transform="translate3d(0,"+(p*k*-100).toFixed(2)+"px,0)";
      });
      tick=false;
    }
    w.addEventListener("scroll",function(){ if(!tick){tick=true;requestAnimationFrame(para);} },{passive:true});
    para();
  }

  /* process steps: rail fill + active step */
  d.querySelectorAll(".steps").forEach(function(steps){
    var fill=steps.querySelector(".steps__fill"), items=[].slice.call(steps.querySelectorAll(".step"));
    function upd(){
      var r=steps.getBoundingClientRect(), mid=w.innerHeight*.55;
      var p=Math.min(1,Math.max(0,(mid-r.top)/r.height));
      if(fill) fill.style.height=(p*100)+"%";
      items.forEach(function(s){ s.classList.toggle("on", s.getBoundingClientRect().top<mid); });
    }
    w.addEventListener("scroll",function(){requestAnimationFrame(upd)},{passive:true}); upd();
  });

  /* counters */
  d.querySelectorAll("[data-count]").forEach(function(el){
    var end=parseInt(el.dataset.count,10), done=false;
    function run(){ if(done) return; done=true; if(reduce){el.textContent=end;return;}
      var t0=null; function f(t){ if(!t0)t0=t; var p=Math.min(1,(t-t0)/1600); el.textContent=Math.round(end*(1-Math.pow(1-p,3))); if(p<1) requestAnimationFrame(f);} requestAnimationFrame(f); }
    if("IntersectionObserver" in w){ new IntersectionObserver(function(es,o){ if(es[0].isIntersecting){run();o.disconnect();} },{threshold:.6}).observe(el);} else run();
  });

  /* accordion */
  d.querySelectorAll(".acc__q").forEach(function(q){
    q.addEventListener("click",function(){
      var i=q.closest(".acc__i"), o=i.classList.toggle("open");
      q.setAttribute("aria-expanded",o?"true":"false");
    });
  });

  /* project slider: drag + buttons + progress */
  d.querySelectorAll(".pslider").forEach(function(sl){
    var tr=sl.querySelector(".ptrack"), bar=sl.querySelector(".pbar i"), prev=sl.querySelector("[data-prev]"), next=sl.querySelector("[data-next]");
    function step(){ var c=tr.querySelector(".pcard"); return c? c.getBoundingClientRect().width+24 : 400; }
    prev&&prev.addEventListener("click",function(){tr.scrollBy({left:-step(),behavior:reduce?"auto":"smooth"})});
    next&&next.addEventListener("click",function(){tr.scrollBy({left:step(),behavior:reduce?"auto":"smooth"})});
    function prog(){ if(!bar) return; var max=tr.scrollWidth-tr.clientWidth, vis=tr.clientWidth/tr.scrollWidth; bar.style.width=(vis*100)+"%"; bar.style.transform="translateX("+(max>0? (tr.scrollLeft/max)*((1-vis)/vis)*100 : 0)+"%)"; }
    tr.addEventListener("scroll",prog,{passive:true}); w.addEventListener("resize",prog); prog();
    var down=false,sx=0,sl0=0,moved=false;
    tr.addEventListener("pointerdown",function(e){ if(e.pointerType!=="mouse") return; down=true;moved=false;sx=e.clientX;sl0=tr.scrollLeft;tr.classList.add("drag"); });
    w.addEventListener("pointermove",function(e){ if(!down) return; var dx=e.clientX-sx; if(Math.abs(dx)>4) moved=true; tr.scrollLeft=sl0-dx; });
    w.addEventListener("pointerup",function(){ if(!down) return; down=false; tr.classList.remove("drag"); });
    tr.addEventListener("click",function(e){ if(moved){e.preventDefault();e.stopPropagation();moved=false;} },true);
  });

  /* videos: pause off-screen, respect reduced motion */
  d.querySelectorAll("video[data-auto]").forEach(function(v){
    if(reduce){ v.removeAttribute("autoplay"); v.pause(); return; }
    if("IntersectionObserver" in w){
      new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ var p=v.play(); p&&p.catch(function(){});} else v.pause(); }); },{threshold:.05}).observe(v);
    }
  });

  /* forms: prototype validation (dry run, no submission) */
  d.querySelectorAll("form.form").forEach(function(f){
    f.addEventListener("submit",function(e){
      e.preventDefault();
      var ok=true;
      f.querySelectorAll("[required]").forEach(function(el){
        var wrap=el.type==="checkbox"? el.closest(".optin") : el.closest(".fld");
        var bad= el.type==="checkbox" ? !el.checked : !el.value.trim() || (el.type==="email" && !/^\S+@\S+\.\S+$/.test(el.value));
        if(wrap) wrap.classList.toggle("err",bad);
        if(bad) ok=false;
      });
      if(!ok){ var first=f.querySelector(".err input,.err select,.err textarea, .optin.err input"); first&&first.focus(); return; }
      f.classList.add("sent");
      var okm=f.querySelector(".form__ok"); okm&&okm.focus();
    });
  });

  /* service explorer: hover/focus swaps featured image */
  d.querySelectorAll(".sx").forEach(function(sx){
    var big=sx.querySelector(".sx__big"), h=sx.querySelector(".sx__h"), p=sx.querySelector(".sx__p"), tiles=sx.querySelectorAll(".sx__tile"), cur=null;
    tiles[0]&&tiles[0].classList.add("on");
    function show(t){ if(cur===t) return; cur=t; tiles.forEach(function(x){x.classList.toggle("on",x===t)});
      big.classList.add("swap"); setTimeout(function(){ big.src=t.dataset.img; h.textContent=t.dataset.name; p.textContent=t.dataset.short; big.onload=function(){big.classList.remove("swap")}; if(big.complete) big.classList.remove("swap"); },220); }
    tiles.forEach(function(t){ t.addEventListener("mouseenter",function(){show(t)}); t.addEventListener("focus",function(){show(t)}); });
  });

  /* year */
  d.querySelectorAll("[data-year]").forEach(function(el){el.textContent=new Date().getFullYear()});

  /* area map: tap a pin to zoom in, labels keep a steady on-screen size */
  d.querySelectorAll("[data-amap]").forEach(function(box){
    var svg=box.querySelector("svg"), FULL=box.dataset.amap.split(" ").map(Number), cur=FULL.slice(), raf=0, active=null;
    var nameEl=box.querySelector("[data-am-name]"), metaEl=box.querySelector("[data-am-meta]"),
        go=box.querySelector("[data-am-go]"), reset=box.querySelector("[data-am-reset]"), bar=box.querySelector("[data-am-scale]");
    function fit(vb){ /* viewBox with the box's aspect so the target stays centred (svg uses slice) */
      var w=box.clientWidth||1, h=box.clientHeight||1, a=w/h, cx=vb[0]+vb[2]/2, cy=vb[1]+vb[3]/2, vw=vb[2], vh=vb[3];
      if(vw/vh>a) vh=vw/a; else vw=vh*a;
      return [cx-vw/2, cy-vh/2, vw, vh];
    }
    function apply(vb){
      cur=vb; svg.setAttribute("viewBox",vb.map(function(n){return n.toFixed(1)}).join(" "));
      var s=box.clientWidth/vb[2]; /* screen px per map unit */
      var target=box.clientWidth<560?.72:.95;
      svg.style.setProperty("--ls",(target/s).toFixed(3));
      if(bar) bar.style.width=Math.round(75*s)+"px"; /* 5 mi = 75 units */
    }
    function animate(to){
      cancelAnimationFrame(raf);
      if(reduce){apply(to);return;}
      var from=cur.slice(), t0=performance.now(), dur=850;
      (function step(t){
        var k=Math.min(1,(t-t0)/dur), e=1-Math.pow(1-k,3);
        apply(from.map(function(v,i){return v+(to[i]-v)*e}));
        if(k<1) raf=requestAnimationFrame(step);
      })(t0);
    }
    function full(){
      if(active) active.classList.remove("on"); active=null;
      box.classList.remove("zoomed");
      nameEl.textContent="Full service area"; metaEl.textContent="Office in Campbell, CA";
      go.hidden=true; reset.hidden=true;
      animate(fit(FULL));
    }
    function zoom(pin){
      if(active===pin){full();return;}
      if(active) active.classList.remove("on");
      active=pin; pin.classList.add("on"); box.classList.add("zoomed");
      var x=+pin.dataset.x, y=+pin.dataset.y;
      nameEl.textContent=pin.dataset.name; metaEl.textContent=pin.dataset.meta;
      if(pin.dataset.href){go.hidden=false; go.href=pin.dataset.href; go.textContent=pin.dataset.name+" page";} else go.hidden=true;
      reset.hidden=false;
      animate(fit([x-150,y-150,300,300]));
    }
    box.querySelectorAll(".am-pin").forEach(function(pin){
      pin.addEventListener("click",function(){zoom(pin)});
      pin.addEventListener("keydown",function(e){ if(e.key==="Enter"||e.key===" "){e.preventDefault();zoom(pin);} });
    });
    reset.addEventListener("click",full);
    box.addEventListener("keydown",function(e){ if(e.key==="Escape"&&active){full();} });
    var rT; w.addEventListener("resize",function(){ clearTimeout(rT); rT=setTimeout(function(){
      if(active) apply(fit([+active.dataset.x-150,+active.dataset.y-150,300,300])); else apply(fit(FULL));
    },120); });
    apply(fit(FULL));
  });

  /* ===== inner pages: scroll-linked motion (reading bar, word fill, photo parallax, closing band) ===== */
  if(d.body.classList.contains("inner")){
    var bar=d.createElement("div"); bar.className="readbar"; bar.setAttribute("aria-hidden","true"); d.body.appendChild(bar);
    d.querySelectorAll(".acc").forEach(function(a){
      [].forEach.call(a.querySelectorAll(".acc__i"),function(it,i){ it.style.setProperty("--i",Math.min(i,10)); });
    });
    var clamp=function(v){return v<0?0:v>1?1:v;};
    var fills=[], pars=[], band=null, bandImg=null;
    var RND=getComputedStyle(document.documentElement).getPropertyValue("--round").trim()==="0"?0:1; /* v2 sets --round:0 for square corners */
    if(!reduce){
      fills=[].map.call(d.querySelectorAll("main h2[data-split]"),function(h){
        h.classList.add("fillh");
        return {el:h, ws:[].slice.call(h.querySelectorAll(".w>span"))};
      });
      pars=[].filter.call(d.querySelectorAll("main .img img, main .xcard__img img, .cstrip__th img, main .dbg img"),function(im){ return !im.hasAttribute("data-para"); });
      band=d.querySelector(".fband__panel"); bandImg=band&&band.querySelector(".fband__bg img");
    }
    var itk=false;
    function iframe(){
      itk=false;
      var vh=w.innerHeight, max=d.documentElement.scrollHeight-vh;
      bar.style.transform="scaleX("+(max>0?(w.scrollY/max).toFixed(4):0)+")";
      fills.forEach(function(f){ /* words fill from faint to solid between 88% and 50% of the viewport */
        var r=f.el.getBoundingClientRect(); if(r.bottom<-80||r.top>vh+80) return;
        var p=clamp((vh*.88-r.top)/(vh*.38)), n=f.ws.length||1;
        f.ws.forEach(function(s,i){ var a=i/n*.7, wp=clamp((p-a)/.3); s.style.opacity=(.16+.84*wp).toFixed(3); });
      });
      pars.forEach(function(im){ /* slow drift: -6% to +6% while the photo crosses the screen */
        var r=im.parentElement.getBoundingClientRect(); if(r.bottom<0||r.top>vh) return;
        var p=clamp((vh-r.top)/(vh+r.height));
        im.style.transform="translate3d(0,"+((p-.5)*12).toFixed(2)+"%,0) scale(1.12)";
      });
      if(band){ /* closing band opens from an inset rounded panel to full size, photo zooms out */
        var br=band.getBoundingClientRect();
        if(br.top<vh+40&&br.bottom>-40){
          var q=clamp((vh*.96-br.top)/(vh*.34));
          band.style.clipPath=q>=1?"":"inset("+(5*(1-q)).toFixed(2)+"% "+(3*(1-q)).toFixed(2)+"% round "+((56-16*q)*RND).toFixed(1)+"px)";
          if(bandImg){ var z=clamp((vh-br.top)/(vh+br.height)); bandImg.style.transform="scale("+(1.2-.16*z).toFixed(3)+")"; }
        }
      }
    }
    var ireq=function(){ if(!itk){itk=true;requestAnimationFrame(iframe);} };
    w.addEventListener("scroll",ireq,{passive:true});
    w.addEventListener("resize",ireq);
    iframe();
  }
})();
