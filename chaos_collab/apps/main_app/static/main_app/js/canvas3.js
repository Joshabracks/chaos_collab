(function (fn) {
  var tool;
  var canvas = fn('paint');
  var ctx = canvas.getContext('2d');

  var history = {
    redo_list: [],
    undo_list: [],
    saveState: function (canvas, list, keep_redo) {
      keep_redo = keep_redo || false;
      if (!keep_redo) {
        this.redo_list = [];
      }

      (list || this.undo_list).push(canvas.toDataURL());
    },
    undo: function (canvas, ctx) {
      this.restoreState(canvas, ctx, this.undo_list, this.redo_list);
    },
    redo: function (canvas, ctx) {
      this.restoreState(canvas, ctx, this.redo_list, this.undo_list);
    },
    restoreState: function (canvas, ctx, pop, push) {
      if (pop.length) {
        this.saveState(canvas, push, true);
        var restore_state = pop.pop();
        var img = new Element('img', { 'src': restore_state });
        img.onload = function () {
          ctx.clearRect(0, 0, 1200, 720);
          ctx.drawImage(img, 0, 0, 1200, 720, 0, 0, 1200, 720);
        }
      }
    }
  }

  var pencil = {
    options: {
      stroke_color: 'rgb(0,255,0)',
      dim: 200
    },



    init: function (canvas, ctx) {
      this.canvas = canvas;
      this.canvas_coords = this.canvas.getCoordinates();
      this.ctx = ctx;
      this.ctx.strokeColor = this.options.stroke_color;
      this.drawing = false;
      this.addCanvasEvents();
    },
    addCanvasEvents: function () {
      this.canvas.addEvent('mousedown', this.start.bind(this));
      this.canvas.addEvent('mousemove', this.stroke.bind(this));
      this.canvas.addEvent('mouseup', this.stop.bind(this));
      this.canvas.addEvent('mouseout', this.stop.bind(this));
    },
    start: function (evt) {
      var x = evt.page.x - this.canvas_coords.left;
      var y = evt.page.y - this.canvas_coords.top;
      this.ctx.beginPath();
      this.ctx.moveTo(x, y);
      history.saveState(this.canvas);
      this.drawing = true;
    },
    stroke: function (evt) {
      if (this.drawing) {
        var x = evt.page.x - this.canvas_coords.left;
        var y = evt.page.y - this.canvas_coords.top;
        this.ctx.lineTo(x, y);
        this.ctx.stroke();
        this.ctx.strokeStyle = this.options.stroke_color;

      }
    },
    stop: function (evt) {
      if (this.drawing) this.drawing = false;
    }
  };

  fn('pencil').addEvent('click', function () {
    pencil.init(canvas, ctx);
  });

  fn('undo').addEvent('click', function () {
    history.undo(canvas, ctx);
  });

  fn('redo').addEvent('click', function () {
    history.redo(canvas, ctx);
  });



  fn('color_listener').addEvent('click', function (e) {
    pencil.options.stroke_color = e.target.id;
    console.log('clicked')
    console.log(e)
    $('#current_color').css('background-color', e.target.id)
  });

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      if (!(/^http:./.test(settings.url) || /^https:./.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });

  $('#publish').on('click', function () {
    history.undo(canvas, ctx)
    console.log("FULL REDO LIST")
    console.log(history.redo_list)
    console.log("REDO LIST SINGLE ELEMENT")
    console.log(history.redo_list[0])
    $.ajax({
      type: "POST",
      url: "/create_collab",
      data: {
        "encoded_img": history.redo_list[0],
      },
      success: window.location.href = "/landing"
    })
    history.redo(canvas, ctx)
  })

  // fn($(document).ready(function(){
  //   console.log("inside ajax call")
  //   $.ajax({
  //     url: "/populate_collab",
  //     success: function(data) {
  //       console.log("success")
  //       console.log(data)
  //       history.redo_list.push(data)
  //       history.redo()
  //     }
    
  // })


})(document.id)



  // original code written by https://codepen.io/abidibo/