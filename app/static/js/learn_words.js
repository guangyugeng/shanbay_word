var log = function() {
  console.log(arguments)
}


var bindEventWordSetting = function() {
    // 绑定用户登录按钮事件
  log("3213")

  $("#setting-word").on('click', function(event){

      // get values from FORM
      log('sdfds')
      log(event.target.id)
      var quota = $("select#id-quota").val()
      var form = {
              quota: quota
      }
//      var weiboId = $(this).data('id')
//      log(weiboId)
//      // 得到整个微博条目的标签
//      var weiboCell = $(this).closest('.weibo-cell')
//      // 调用 api.weiboDelete 函数来删除微博并且在删除成功后删掉页面上的元素
      log("1111")
      api.wordSetting(form, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              console.log('成功', arguments)
              alert("修改成功")

              location.href = "http://" + location.host + "/word"
              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}


var bindEventWordbookAdd = function() {
    // 绑定用户登录按钮事件
  log("3213")

  $("#add-wordbook").on('click', function(){

       var book_name = $("#book_name").val();
//       var message = $("textarea#message").val();
//       var firstName = name; // For Success/Failure Message
//       // Check for white space in name for Success/Fail message
//       if (firstName.indexOf(' ') >= 0) {
//           firstName = name.split(' ').slice(0, -1).join(' ');
//       }
       log(book_name,"1123")
       var form = {
           book_name: book_name
       };
//       log(form.wordbook)
       api.wordbookAdd(form, function(response) {
           // 直接用一个匿名函数当回调函数传给 weiboDelete
           // 这是 js 常用的方式
           var r = response
           if(r.success) {
//                   console.log('注册成功', arguments)
               alert("增加成功")
               location.href = "http://" + location.host + "/wordbook"
               // slideUp 可以以动画的形式删
           } else {
              console.log('错误', arguments)
               alert(r.message)
           }
       })
  })
}


var bindEventWordbookChoice = function() {
    // 绑定用户登录按钮事件
  log("3213")

  $(".my-wordbook").on('click', function(event){

      // get values from FORM
      log('sdfds')
      log(event.target.id)
      var form = {
              book_name: event.target.id
      }
//      var weiboId = $(this).data('id')
//      log(weiboId)
//      // 得到整个微博条目的标签
//      var weiboCell = $(this).closest('.weibo-cell')
//      // 调用 api.weiboDelete 函数来删除微博并且在删除成功后删掉页面上的元素
      log("1111")
      api.wordbookChoice(form, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              console.log('成功', arguments)
              alert("修改成功")

              location.href = "http://" + location.host + "/wordbook"
              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
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
    // 展开评论事件
    log('note')

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
    // 绑定用户登录按钮事件
  log("start")

  $(".word-container").on('click', "#start-learn", function(){

      // get values from FORM
      log('sdfds')
      var startCell = $(this).closest('.start-cell')
      log("1111")
      api.wordsStartLearn(function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              $(startCell).remove()
              var w = r.data
              $('.word-container').prepend(wordTemplate(w))

              console.log('成功', arguments)
//              alert("修改成功")

//              location.href = "http://" + location.host + "/wordbook"
              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}


var bindEventWordsKnown = function() {
    // 绑定用户登录按钮事件
  log("learn")

  $(".word-container").on('click', ".known", function(event){

      // get values from FORM
      log('known')
      log("1111")
      var wordCell = event.target.closest('.word-cell')
      word = $(wordCell).find("p").text()
//      log(word.text())
      form = { word:word }
      api.wordsKnown(form, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              log('成功')
//              alert("修改成功")
//              log(wordCell.nodeName)
              $(wordCell).remove()
              var w = r.data
              var mns = r.data2
              var uns = r.data3
              $('.word-container').prepend(word_mine_userDetailTemplate(w, mns, uns))


              // slideUp 可以以动画的形式删掉一个元

          } else {

              console.log('错误', arguments)
              alert(r.message)
              location.href = "http://" + location.host + "/word"

          }
      })
  })
}


var bindEventWordsUnknown = function() {
    // 绑定用户登录按钮事件
  log("learn")

  $(".word-container").on('click', ".unknown", function(event){

      // get values from FORM
      log('unknown')
      log("1111")
      var wordCell = event.target.closest('.word-cell')
      var word = $(wordCell).find("p").text()
//      log(word.text())
      var form = { word:word }
      log(form)
      log(form['word'])
      log(form[word])
      api.wordsUnknown(form, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              log('成功')
//              alert("修改成功")
//              log(wordCell.nodeName)
              $(wordCell).remove()
              var w = r.data
              var mns = r.data2
              var uns = r.data3
              log(uns.push)
              $('.word-container').prepend(word_mine_userDetailTemplate(w, mns, uns))




              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
              alert(r.message)
              location.href = "http://" + location.host + "/word"

          }
      })
  })
}



var bindEventWordDetail = function() {
    // 绑定用户登录按钮事件
  log("learn")

  $(".word-container").on('click', ".continue", function(event){

      // get values from FORM
      log('continue')
      log("1111")
      api.wordsDetail(function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              log('继续成功')
//              alert("修改成功")
              var wordDetailCell = event.target.closest('.word-detail-cell')
//              log(wordCell.nodeName)
              $(wordDetailCell).remove()
              var w = r.data
              $('.word-container').prepend(wordTemplate(w))

              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
              alert(r.message)
              location.href = "http://" + location.host + "/word"
          }
      })
  })
}


var bindEventNoteAdd = function() {
    // 绑定用户登录按钮事件
  log("learn")

  $(".word-container").on('click', "#add-note", function(event){

      // get values from FORM
      log('continue')
      log("1111")

      var wordCell = event.target.closest('.word-detail-cell')

      var word = $(wordCell).find("p#word-name").text()
      var note = $("input#note-input").val()
      log('word',word)
      var form = {
          word: word,
          note: note
      }

      api.noteAdd(form, function(response) {
          // 直接用一个匿名函数当回调函数传给 weiboDelete
          // 这是 js 常用的方式
          var r = response
          if(r.success) {
              log('笔记增加成功')
//              var wordDetailCell = event.target.closest('.word-detail-cell')
////              log(wordCell.nodeName)
//              $(wordDetailCell).remove()
              var n = r.data
              log(event.target.nodeName)
              var mineBox = $(wordCell).find("div#note-mine-box")
              var userBox = $(wordCell).find("div#note-user-box")

              log(mineBox)
              $(mineBox).prepend(noteTemplate(n))
              $(userBox).prepend(noteTemplate(n))




              // slideUp 可以以动画的形式删掉一个元

          } else {
              console.log('错误', arguments)
              alert(r.message)
          }
      })
  })
}
//   }
//          */
//          // arguments 是包含所有参数的一个 list
//          console.log('成功', arguments)
//          log(r)
//          if(r.success) {
//              // 如果成功就添加到页面中
//              // 因为添加微博会返回已添加的微博数据所以直接用 r.data 得到
//              var w = r.data
//              $('.weibo-container').prepend(weiboTemplate(w))
//              alert("添加成功")
//          } else {
//              // 失败，弹出提示
//              alert(r.message)
//          }
//      }
//    $('.weibo-container').on('click', '.weibo-delete', function(){
//      // 得到当前的 weibo_id
//      var weiboId = $(this).data('id')
//      log(weiboId)
//      // 得到整个微博条目的标签
//      var weiboCell = $(this).closest('.weibo-cell')
//
//      // 调用 api.weiboDelete 函数来删除微博并且在删除成功后删掉页面上的元素
//      api.weiboDelete(weiboId, function(response) {
//          // 直接用一个匿名函数当回调函数传给 weiboDelete
//          // 这是 js 常用的方式
//          var r = response
//          if(r.success) {
//              console.log('成功', arguments)
//              // slideUp 可以以动画的形式删掉一个元素
//              $(weiboCell).slideUp()
//              alert("删除成功")
//          } else {
//              console.log('错误', arguments)
//              alert("删除失败")
//          }


var bindEvents = function() {
    // 不同的事件用不同的函数去绑定处理
    // 这样逻辑就非常清晰了
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

// 页面载入完成后会调用这个函数，所以可以当做入口
$(document).ready(function(){
    // 用 bindEvents 函数给不同的功能绑定事件处理
    // 这样逻辑就非常清晰了
    log("333")
    bindEvents()
})
