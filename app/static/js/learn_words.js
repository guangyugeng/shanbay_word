var log = function() {
  console.log(arguments)
}


var bindEventWordSetting = function() {

  $("#setting-word").on('click', function(event){

      var quota = $("select#id-quota").val()
      var form = {
              quota: quota
      }

      api.wordSetting(form, function(response) {
          var r = response
          if(r.success) {
              console.log('成功', arguments)
              alert("修改成功")
              location.href = "http://" + location.host + "/word"
          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}


var bindEventWordbookAdd = function() {

  $("#add-wordbook").on('click', function(){

       var book_name = $("#book_name").val();
       log(book_name,"1123")
       var form = {
           book_name: book_name
       };
       api.wordbookAdd(form, function(response) {
           var r = response
           if(r.success) {
               alert("增加成功")
           } else {
              console.log('错误', arguments)
               alert(r.message)
           }
       })
  })
}


var bindEventWordbookChoice = function() {

  $(".my-wordbook").on('click', function(event){

      var form = {
              book_name: event.target.id
      }
      api.wordbookChoice(form, function(response) {
          var r = response
          if(r.success) {
              alert("选择成功")
              location.href = "http://" + location.host + "/wordbook"

          } else {
              alert(r.message)
          }
      })
  })
}


var wordTemplate = function(word) {
  var w = word
  var t = `
    <div class="word-cell cell item "">
      <p>${ w.word }</p>
      <div class="row">

          <button class="known btn btn-success btn-lg">认识</button>
          <button class="unknown btn btn-success btn-lg">不认识</button>

      </div>
    </div>
  `
  return t
}

var noteTemplate = function(note) {
  var n = note
  var t = `
     <div class="content note-cell">
     <span>${ n.note }</span>
     <div class="author">作者 ${ n.learner }</div>
     </div>
  `
  return t
}

var word_mine_userDetailTemplate = function(word, mine_notes, user_notes) {
  var w = word
  var mns = mine_notes
  var uns = user_notes
  var t = (mns, uns) => `

    <div class="word-detail-cell cell item "">
      <p id="word-name">${ w.word }</p>
      <p>${ w.translated }</p>
      <p>${ w.example }</p>
      <p>${ w.example_cn }</p>

      <ul id="note-tab" class="nav nav-tabs">
         <li class=""><a class="note-mine-box-item" href="#note-mine-box">我的笔记</a></li>
         <li class=""><a class="note-user-box-item" href="#note-user-box">共享笔记</a></li>
         <li class=""><a class="note-create-box-item" href="#note-create-box">创建笔记</a></li>
      </ul>

      <div class='note-content'>
        <div id="note-mine-box" class="note-content-item hide note-mine-box-item">
          <br>
           ${mns.map(mn => `

            <div class="content note-cell">
            <span>${ mn.note }</span>
            <div class="author">作者 ${ mn.learner }</div>
            </div>
            <br><br>
           `).join('')}
        </div>
        <div id="note-user-box" class="note-content-item hide note-user-box-item">
          <br>
           ${uns.map(un => `

            <div class="content note-cell">
            <span>${ un.note }</span>
            <div class="author">作者 ${ un.learner }</div>
            </div>
            <br><br>
           `).join('')}
        </div>
        <div id="note-create-box" class="note-content-item hide note-create-box-item">
            <br>
            <input id="note-input" name="comment" class="left m form-control" placeholder="note">
            <br>
            <button id="add-note" class="btn btn-success btn-lg">增加笔记</button>
        </div>
      </div>
      <br>
      <div class="row">

          <button class="continue btn btn-success btn-lg">继续</button>

      </div>
    </div>
  `
  return t(mns,uns)
}


var bindEventNoteToggle = function(){

    $(".word-container").on("click", "ul.nav-tabs li" ,function(event) {
        log('Toggle')
        $("ul.nav-tabs li").removeClass("active");
        $(this).addClass("active");
        $(".note-content-item").addClass("hide");
        var activeTab = $(this).find("a").attr("href");
        $(activeTab).removeClass("hide");
        log('pass')
        return false;
    });

}


var bindEventStartLearn = function() {

  $(".word-container").on('click', "#start-learn", function(){

      var startCell = $(this).closest('.start-cell')

      api.wordsStartLearn(function(response) {
          var r = response
          if(r.success) {
              $(startCell).remove()
              var w = r.data
              $('.word-container').prepend(wordTemplate(w))
          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}


var bindEventWordsKnown = function() {

  $(".word-container").on('click', ".known", function(event){

      var wordCell = event.target.closest('.word-cell')
      word = $(wordCell).find("p").text()
      form = { word:word }

      api.wordsKnown(form, function(response) {
          var r = response
          if(r.success) {
              $(wordCell).remove()
              var w = r.data
              var mns = r.data2
              var uns = r.data3
              $('.word-container').prepend(word_mine_userDetailTemplate(w, mns, uns))
          } else {
              console.log('错误', arguments)
              alert(r.message)
              location.href = "http://" + location.host + "/word"
          }
      })
  })
}


var bindEventWordsUnknown = function() {

  $(".word-container").on('click', ".unknown", function(event){

      var wordCell = event.target.closest('.word-cell')
      var word = $(wordCell).find("p").text()
      var form = { word:word }

      api.wordsUnknown(form, function(response) {
          var r = response
          if(r.success) {
              $(wordCell).remove()
              var w = r.data
              var mns = r.data2
              var uns = r.data3
              $('.word-container').prepend(word_mine_userDetailTemplate(w, mns, uns))
          } else {
              alert(r.message)
              location.href = "http://" + location.host + "/word"

          }
      })
  })
}


var bindEventWordDetail = function() {

  $(".word-container").on('click', ".continue", function(event){

      api.wordsDetail(function(response) {

          var r = response
          if(r.success) {
              log('继续成功')
              var wordDetailCell = event.target.closest('.word-detail-cell')
              $(wordDetailCell).remove()
              var w = r.data
              $('.word-container').prepend(wordTemplate(w))
          } else {
              alert(r.message)
              location.href = "http://" + location.host + "/word"
          }
      })
  })
}


var bindEventNoteAdd = function() {

  $(".word-container").on('click', "#add-note", function(event){

      var wordCell = event.target.closest('.word-detail-cell')
      var word = $(wordCell).find("p#word-name").text()
      var note = $("input#note-input").val()
      var form = {
          word: word,
          note: note
      }

      api.noteAdd(form, function(response) {
          var r = response
          if(r.success) {
              var n = r.data
              log(event.target.nodeName)
              var mineBox = $(wordCell).find("div#note-mine-box")
              var userBox = $(wordCell).find("div#note-user-box")

              $(mineBox).prepend(noteTemplate(n))
              $(userBox).prepend(noteTemplate(n))
          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}


var bindEvents = function() {

    bindEventWordSetting()
    bindEventWordbookChoice()
    bindEventStartLearn()
    bindEventWordsKnown()
    bindEventWordsUnknown()
    bindEventWordDetail()
    bindEventNoteAdd()
    bindEventNoteToggle()
    bindEventWordbookAdd()

}


$(document).ready(function(){

    bindEvents()

})
