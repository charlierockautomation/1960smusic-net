/* site-wide behaviour shared by every page */
(function(){
  /* current year (never goes stale) */
  document.querySelectorAll('[data-year]').forEach(function(e){
    e.textContent = new Date().getFullYear();
  });

  /* mobile hamburger menu: brass toggle -> walnut dropdown panel */
  var toggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav){
    function setOpen(open){
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    }
    toggle.addEventListener('click', function(){
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    /* close after choosing a destination */
    nav.querySelectorAll('a').forEach(function(a){
      a.addEventListener('click', function(){ setOpen(false); });
    });
    /* close on Escape */
    document.addEventListener('keydown', function(e){
      if (e.key === 'Escape' && nav.classList.contains('open')){ setOpen(false); toggle.focus(); }
    });
  }
})();
