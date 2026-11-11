// Kiran Growth School: every enquiry goes to WhatsApp +91 93998 51765
(function(){
  const WA="919399851765",waUrl=m=>"https://wa.me/"+WA+"?text="+encodeURIComponent(m);
  const $=id=>document.getElementById(id);
  // enquiry form -> prefilled WhatsApp message
  const send=$("send");
  if(send){
    const v=id=>($(id)&&$(id).value||"").trim();
    const build=()=>{let m="Hi Kiran Growth School, new website enquiry.\nName: "+(v("nm")||"-")+"\nPhone: "+(v("pn")||"-")+"\nCity: "+(v("ct")||"-")+"\nBusiness: "+(v("tp")||"-")+"\nInterested in: "+(v("it")||"-");if(v("ms"))m+="\nMessage: "+v("ms");m+="\nPage: "+location.pathname;send.href=waUrl(m)};
    ["nm","pn","ct","tp","it","ms"].forEach(id=>$(id)&&$(id).addEventListener("input",build));build();
    const f=$("enq");f&&f.addEventListener("submit",e=>{e.preventDefault();window.open(send.href,"_blank","noopener")});
  }
  document.querySelectorAll(".copy").forEach(b=>b.addEventListener("click",()=>{try{navigator.clipboard.writeText(b.dataset.copy).then(()=>{b.textContent="Copied";setTimeout(()=>b.textContent="Copy",1500)})}catch(e){}}));
  const bg=$("burger"),mob=$("mob");
  if(bg&&mob){bg.addEventListener("click",()=>{const o=mob.classList.toggle("open");bg.setAttribute("aria-expanded",String(o))});
    mob.querySelectorAll("a").forEach(a=>a.addEventListener("click",()=>{mob.classList.remove("open");bg.setAttribute("aria-expanded","false")}))}
  const ph=$("photo");
  if(ph&&!matchMedia("(prefers-reduced-motion: reduce)").matches&&matchMedia("(pointer:fine)").matches){const st=ph.querySelector(".stage");
    ph.addEventListener("mousemove",e=>{const r=ph.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;st.style.transform=`rotateY(${x*14}deg) rotateX(${-y*10}deg)`});
    ph.addEventListener("mouseleave",()=>st.style.transform="")}
})();
