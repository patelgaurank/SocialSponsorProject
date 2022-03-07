'{% if user.is_authenticated %}'
  sessionSecurity.activity();
  window.addEventListener("load", function() { window. scrollTo(0, 0); });
  function bigbar_open() {
    document.getElementById("menu").style.display = "none";
    document.getElementById("allContainer").style.marginLeft = "200px";
    '{% if request.get_full_path == "/sponsor/sponsorform/" %}'
      document.getElementById("sponsorModal").style.marginLeft = "200px";
    '{% endif %}'
    document.getElementById("myBigSidebar").style.display = "block";
  }

  function bigbar_close() {
    document.getElementById("menu").style.display = "block";
    document.getElementById("allContainer").style.marginLeft = "0%";
    '{% if request.get_full_path == "/sponsor/sponsorform/" %}'
      document.getElementById("sponsorModal").style.marginLeft = "0%";
    '{% endif %}'
    document.getElementById("myBigSidebar").style.display = "none";
  }

  var mySidebar = document.getElementById("ssSB");
  function bar_open() {
    if (mySidebar.style.display === 'block') {
      mySidebar.style.display = 'none';
    } else {
      mySidebar.style.display = 'block';
    }
  }

  function bar_close() {
      mySidebar.style.display = "none";
  }
// Do not delete
  // window.addEventListener('resize', function () {
  //     myFunction('resize');
  // });

  // window.addEventListener("orientationchange", function() {
  //     myFunction('orientation');
  // });

  // function myFunction(value) {
  //     var x = 1;
  //     if (value == 'resize') {
  //       // do something
  //       console.log($('#sponsorTableResponsive').height);
  //       console.log('Window resize - '+ window.innerHeight + ' - ' + window.innerWidth);
  //     } else if (value == 'orientation') {
  //       // do something else
  //       console.log('Window Orient - '+ window.innerHeight);
  //     }
  // }

'{% if request.get_full_path == "/sponsor/dashboard/" or request.get_full_path == "/sponsor/display/" %}'
  var locCity, LocState;
  locCity = '{{ userCity }}';
  locState = '{{ userState }}';
  $('#barTitle').text('SPONSOR APP');
'{% endif %}'

'{% if request.get_full_path == "/ims/imsdata/" or request.get_full_path == "/ims/imsform/" %}'
  $('#barTitle').text('IMS APP');
'{% endif %}'


// Run this on open window //
// Open up on page load //
'{% if request.get_full_path != "/accounts/logout/" and request.get_full_path != "/accounts/login/" and request.get_full_path != "/sponsor/display/" %}'
  document.addEventListener('DOMContentLoaded', function() {
    // console.log(getUA());
    // if ( typeof locAddress === 'undefined' ) {
    //   readLocationData();
    //   console.log('Run');
    // }
    const ul1 = document.querySelector('#userList');
    const mnContainer = document.querySelector('#allContainer');
    var loc = window.location;
    var pname = loc.pathname;
    var uLio1, uLio;
    var wsStart = 'ws://';
      if (loc.protocol == 'https:') {
        wsStart = 'wss://';
      }
      const alertSocket = new ReconnectingWebSocket(
        wsStart
        + loc.host
        + loc.pathname
      );
      alertSocket.onmessage = function(e) {
        var setTm;
        var msgIn = JSON.parse(e.data);
        if (msgIn.Desc === 'User Log In/Out.') {

          if ('{{ user.first_name }}' !== msgIn.username) {
            var el = document.createElement("li");
            $('#id_' + msgIn.username).remove();
            var nodeLi, nodeSpan;
            $(ul1).prepend(msgIn.uStatusList);
            $(mnContainer).append(msgIn.uStatus);
          }
        } else if (msgIn.Desc === 'Sponsor Added/Updated') {
          $('#spTotal').text(msgIn.spTotal);
            $('#spTodayTotal').text(msgIn.spTodayTotal);
            $('#dbSpTableBody').prepend(msgIn.spListHTML);
            $(mnContainer).append(msgIn.spStatusHTML);
        }
        setTimeout(function(){
              if ($('#appStatus').length > 0) {
                $('#appStatus').remove();
              }
            }, 3000);
      }

      alertSocket.onopen = function(e) {
        console.log("open message", e);
        // alertSocket.send(locAddress);
      }
      alertSocket.onerror = function(e) {
        console.log("message error", e);
      }

      alertSocket.onclose= function(e) {
        console.log("close message", e);
      }
  });

'{% endif %}'
'{{ request.get_full_path }}'
'{% if request.get_full_path == "/sponsor/sponsordata/" or request.get_full_path == "/sponsor/sponsorform/"  or request.get_full_path == "/sponsor/sharedSponsorform/" or request.get_full_path == "ims/imsform/" %}'
  // Sponsor Form Update Country, State, City list by entering zip
  $("#id_ZipCode").change(function () {
    var url = "{{ request.path }}";
    var zipcodeId = $(this).val();
    $.ajax({
      type: "POST",
      url: url,
      data: {
        csrfmiddlewaretoken: '{{ csrf_token }}',
        zipcode: zipcodeId,
      },
      success: function (data) {
        if (data.is_taken) {
          alert("Location not available.");
        } else {
          $.each( data, function( key, value ) {
              $("#"+key).val(value);
              var el = document.getElementById(key);
              if ( value == 'NA' ) {
                el.readOnly = false;
              } else {
                el.readOnly = true;
              }
          });
        }
      }
    });
  });


  // Sponsor Form Update purpose code list
  $("#id_Purpose").change(function () {
        var url = "{{ request.path }}";
        var purposeId = $(this).val();
        $.ajax({
          type: "POST",
          url: url,
          data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            purpose: purposeId,
          },
          success: function (data) {
            // alert(data);
            if (data.is_taken) {
              alert("Location not available.");
            } else {
              $.each( data, function( key, value ) {
                // console.log(value);
                $.each( value, function( k, v) {
                  if ( k === 'fields' ) {
                    console.log();
                    $("#id_Purpose_Code").val(v['Purpose_Code']);
                    $("#id_PurposeIndex").val(v['Purpose_Index']);
                    $("#id_Memo").val(v['AnnounceAs']);
                    // $.each( v, function( k1, v1 ) {
                    //   console.log(k1);
                    // });
                  }
                });
              });
            }
          },
        });
  });

  // Sponsor Form Input Autocomplete
  $( function() {
    var id;
    var lstValue = [];
    function getListValue( val ) {
      var vl, vlInd;
      vl = val;
      id = id;
      if ((val.indexOf(",")) !== -1) {
        vlInd = (val).lastIndexOf(",")+1;
      } else if ((val.indexOf(" ")) !== -1) {
        vlInd = (val).lastIndexOf(" ")+1;
      } else if ((val.indexOf("&")) !== -1) {
        vlInd = (val).lastIndexOf("&")+1;
      } else {
        vlInd = 0;
      };
      vl = (val).substr(vlInd);
      vl = vl.trim();
      $.ajax({
        url: "{{ request.path }}",
        type: "POST",
        data: {
          csrfmiddlewaretoken: '{{ csrf_token }}',
          lst: id+'-'+vl,
        },
        success: function(data) {
          var result = [];
          data = JSON.parse(data);
          len = data.length;
          for (i = 0; i < len; i++) {
            result.push({
              label: data[i],
              value: data[i]
            });
            lstValue[i] = data[i];
          }
          return lstValue;
        },
      });
    };
    function split( val ) {
      return val.split( /,\s*/ );
    }
    function extractLast( term ) {
      return split( term ).pop();
    }
    $( "input.spFormInput" )
      .on( "keydown", function( event ) {
        id = this.id;
        if ( event.keyCode === $.ui.keyCode.TAB &&
            $( this ).autocomplete( "instance" ).menu.active ) {
          event.preventDefault();
        }
      })
      .autocomplete({
        minLength: 0,
        source: function( request, response ) {
          getListValue( request.term );
          response( $.ui.autocomplete.filter(
            lstValue, extractLast( request.term ) ) );
        },
        focus: function() {
          return false;
        },
        select: function( event, ui ) {
          var terms = split( this.value );
          terms.pop();
          terms.push( ui.item.value );
          terms.push( "" );
          this.value = terms.join( ", " );
          return false;
        }
      });
  } );
'{% endif %}'

  const getUA = () => {
      let device = "Unknown";
      const ua = {
          "Generic Linux": /Linux/i,
          "Android": /Android/i,
          "BlackBerry": /BlackBerry/i,
          "Bluebird": /EF500/i,
          "Chrome OS": /CrOS/i,
          "Datalogic": /DL-AXIS/i,
          "Honeywell": /CT50/i,
          "iPad": /iPad/i,
          "iPhone": /iPhone/i,
          "iPod": /iPod/i,
          "macOS": /Macintosh/i,
          "Windows": /IEMobile|Windows/i,
          "Zebra": /TC70|TC55/i,
      }
      Object.keys(ua).map(v => navigator.userAgent.match(ua[v]) && (device = v));
      return device;
  }

'{% endif %}'

'{% block script %}'
'{% endblock script %}'