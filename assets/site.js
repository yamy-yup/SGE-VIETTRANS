(function(){
  var $=function(s,c){return (c||document).querySelector(s)};
  var $$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};

  /* Menu trên điện thoại */
  var mb=$('#menu-btn'),nav=$('#nav');
  function closeAll(){
    nav.classList.remove('open');
    mb.setAttribute('aria-expanded','false');mb.setAttribute('aria-label','Mở menu');
    $$('.dd',nav).forEach(function(d){d.classList.remove('open');$('.dd-btn',d).setAttribute('aria-expanded','false')});
  }
  mb.addEventListener('click',function(){
    var o=nav.classList.toggle('open');
    mb.setAttribute('aria-expanded',o?'true':'false');
    mb.setAttribute('aria-label',o?'Đóng menu':'Mở menu');
  });

  /* Menu xổ xuống: bấm mũi tên để mở, bấm ra ngoài hoặc Esc để đóng */
  $$('.dd',nav).forEach(function(d){
    var btn=$('.dd-btn',d);
    btn.addEventListener('click',function(e){
      e.stopPropagation();
      var o=!d.classList.contains('open');
      $$('.dd',nav).forEach(function(x){x.classList.remove('open');$('.dd-btn',x).setAttribute('aria-expanded','false')});
      d.classList.toggle('open',o);
      btn.setAttribute('aria-expanded',o?'true':'false');
    });
  });
  document.addEventListener('click',function(e){
    if(!nav.contains(e.target)&&!mb.contains(e.target))closeAll();
  });
  document.addEventListener('keydown',function(e){
    if(e.key==='Escape'){closeAll();if(document.activeElement&&nav.contains(document.activeElement))document.activeElement.blur()}
  });
  $$('a',nav).forEach(function(a){a.addEventListener('click',function(){closeAll();a.blur()})});

  var yr=$('#year');if(yr)yr.textContent=new Date().getFullYear();

  /* ===== Chuyển động ===== */
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Thanh menu đổ bóng khi cuộn */
  var bar=$('.bar');
  function onBar(){if(bar)bar.classList.toggle('scrolled',window.scrollY>12)}
  window.addEventListener('scroll',onBar,{passive:true});onBar();

  /* Ảnh đầu trang trôi nhẹ khi cuộn (chỉ màn hình lớn) */
  var heroPic=$('.hero picture'),ticking=false;
  if(heroPic&&!reduce&&window.matchMedia('(min-width: 761px)').matches){
    window.addEventListener('scroll',function(){
      if(ticking)return;ticking=true;
      requestAnimationFrame(function(){
        var y=Math.min(window.scrollY,900);
        heroPic.style.transform='translate3d(0,'+(y*0.18).toFixed(1)+'px,0) scale('+(1+y*0.00008).toFixed(4)+')';
        ticking=false;
      });
    },{passive:true});
  }

  /* Hiện dần nội dung khi cuộn tới */
  var SEL=['.intro .grid > div','.pledge li','.promo-txt .box','.team .grid > div','.how .head','.steps li','.q-left','.q-right',
    '.faq .grid > *','.contact .grid > *','.page-head h1','.page-head .lead','.page-head .head-act','.page-head .meta',
    '.prose > section','.prose > .toc-box','.prose > .post-cta','.side > *','.svc-cards li','.cards .card','.rows li','.filters'];
  var CLIP=['.intro figure','.prose > .fig','.svc-cards .fig'];
  if(!reduce&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('is-in');io.unobserve(e.target)}});
    },{rootMargin:'0px 0px -8% 0px',threshold:.08});
    var vh=window.innerHeight;
    function prep(list,cls){
      $$(list.join(',')).forEach(function(el){
        var r=el.getBoundingClientRect();
        var sib=el.parentNode?Array.prototype.indexOf.call(el.parentNode.children,el):0;
        el.style.setProperty('--d',Math.min(sib,6)*70+'ms');
        el.classList.add(cls);
        if(r.top<vh*0.95){requestAnimationFrame(function(){requestAnimationFrame(function(){el.classList.add('is-in')})})}
        else io.observe(el);
      });
    }
    prep(SEL,'rv');prep(CLIP,'rv-clip');
    /* Dự phòng: phần tử nào đã lọt vào màn hình (kể cả khi cuộn nhanh) thì hiện ngay */
    var pend=false;
    function sweep(){pend=false;var lim=window.innerHeight*0.98,end=window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4;
      $$('.rv:not(.is-in),.rv-clip:not(.is-in)').forEach(function(el){if(end||el.getBoundingClientRect().top<lim){el.classList.add('is-in');io.unobserve(el)}})}
    window.addEventListener('scroll',function(){if(!pend){pend=true;setTimeout(sweep,140)}},{passive:true});
    window.addEventListener('resize',sweep);
  }

  /* Ảnh hiện mềm khi tải xong */
  $$('img[loading="lazy"]').forEach(function(im){
    if(im.complete)return;
    im.classList.add('loading');document.documentElement.classList.add('js-img');
    im.addEventListener('load',function(){im.classList.remove('loading')},{once:true});
    im.addEventListener('error',function(){im.classList.remove('loading')},{once:true});
  });
})();
