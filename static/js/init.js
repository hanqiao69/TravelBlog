(function($) {

  skel.init({
    reset: 'full',
    breakpoints: {
      'global': { range: '*', href: '../css/style.css', containers: 1200, grid: { gutters: 0 } },
      'normal': { range: '-1280', href: '../css/style-normal.css', containers: 960, grid: { gutters: 0 } },
      'narrow': { range: '-1080', href: '../css/style-narrow.css', containers: '100%' },
      'narrower': { range: '-820', href: '../css/style-narrower.css', containers: '100%!', grid: { gutters: 0 } },
      'mobile': { range: '-736', href: '../css/style-mobile.css', viewport: { scalable: false } },
      'mobilep': { range: '-480', href: '../css/style-mobilep.css', grid: { gutters: 0 } }
    },
    plugins: {
      layers: {
        config: {
          mode: 'transform'
        },
        navPanel: {
          hidden: true,
          breakpoints: 'mobile',
          position: 'top-left',
          side: 'top',
          animation: 'pushY',
          width: '100%',
          height: { mobilep: 300, mobile: 180 },
          clickToHide: true,
          swipeToHide: false,
          html: '<a href="index.html" class="link depth-0">Home</a><div data-action="navList" data-args="nav"></div>',
          orientation: 'vertical'
        },
        navButton: {
          breakpoints: 'mobile',
          position: 'top-center',
          side: 'top',
          height: 50,
          width: 100,
          html: '<div class="toggle" data-action="toggleLayer" data-args="navPanel"></div>'
        }
      }
    }
  });

})(jQuery);