// Kiran Growth School: every enquiry goes to WhatsApp +91 93998 51765
(function(){
  const WA="919399851765",waUrl=m=>"https://wa.me/"+WA+"?text="+encodeURIComponent(m);
  const $=id=>document.getElementById(id);
  // every lead form (.lf) -> prefilled WhatsApp message
  const lbl={nm:"Name",pn:"Phone",ct:"City",bz:"Business",tp:"Business type",it:"Interested in",ms:"Message"};
  document.querySelectorAll("form.lf").forEach(f=>{
    f.addEventListener("submit",e=>{
      e.preventDefault();
      const pn=f.querySelector('[name="pn"]');
      if(pn&&pn.value.replace(/\D/g,"").length<10){pn.focus();pn.setCustomValidity("Please enter a 10-digit phone number");pn.reportValidity();setTimeout(()=>pn.setCustomValidity(""),2000);return}
      let m="Hi Kiran Growth School, new website enquiry.";
      Object.keys(lbl).forEach(k=>{const el=f.querySelector('[name="'+k+'"]');if(el&&el.value.trim())m+="\n"+lbl[k]+": "+el.value.trim()});
      m+="\nPage: "+location.pathname+(f.dataset.src?" ("+f.dataset.src+")":"");
      if(window.gtag)try{gtag("event","generate_lead",{form:f.dataset.src||"form"})}catch(_){}
      window.open(waUrl(m),"_blank","noopener");
    });
  });
  document.querySelectorAll(".copy").forEach(b=>b.addEventListener("click",()=>{try{navigator.clipboard.writeText(b.dataset.copy).then(()=>{b.textContent="Copied";setTimeout(()=>b.textContent="Copy",1500)})}catch(e){}}));
  const bg=$("burger"),mob=$("mob");
  if(bg&&mob){bg.addEventListener("click",()=>{const o=mob.classList.toggle("open");bg.setAttribute("aria-expanded",String(o))});
    mob.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{mob.classList.remove("open");bg.setAttribute("aria-expanded","false")}))}
  const ph=$("photo");
  if(ph&&!matchMedia("(prefers-reduced-motion: reduce)").matches&&matchMedia("(pointer:fine)").matches){const st=ph.querySelector(".stage");
    ph.addEventListener("mousemove",e=>{const r=ph.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;st.style.transform=`rotateY(${x*14}deg) rotateX(${-y*10}deg)`});
    ph.addEventListener("mouseleave",()=>st.style.transform="")}
})();
