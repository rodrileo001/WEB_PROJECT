//////////////////////////////////////////////////////////////////////////////////////////////////////////////// 
// Chad McLain
// Assignment 4
// 
// 
/////////////////////////////////////////////////////////////////////////////////////////////////////////


//Keep count of how many movies are in a list
// var keyCount = Object.keys(movie_obj).length;
// alert(keyCount);


// ----------------------NavBar (main)
const homeTab = document.getElementById("homeTab")
const searchTab = document.getElementById('searchTab')

// homeTab.addEventListener('click', function () {
//     homeTab.classList.add('active')
//     searchTab.classList.remove('active')
// })
// homeTab.addEventListener('click', function () {
//     searchTab.classList.add('active')
//     homeTab.classList.remove('active')
// })


// console.log(movie_genre)

// ---------------------  SEARCH

//  Set Search By Field (Title, Year, Cast)
var search_by = "title";
document.getElementById("searchTitle").addEventListener("click", function () {
    var inputText = document.getElementById("movieSearch");
    inputText.value = "";
    inputText.setAttribute("placeholder", "Title")
    search_by = "title";
    this.classList.add('active')
    document.getElementById("searchYear").classList.remove("active")
    document.getElementById("searchGenres").classList.remove("active")
    document.getElementById("searchCast").classList.remove("active")
    // appendData(default_list, 0);
    appendData(movie_obj, 0);
})
document.getElementById("searchYear").addEventListener("click", function () {
    var inputText = document.getElementById("movieSearch");
    inputText.value = "";
    inputText.setAttribute("placeholder", "Year")
    search_by = "year";
    this.classList.add('active')
    document.getElementById("searchTitle").classList.remove("active")
    document.getElementById("searchGenres").classList.remove("active")
    document.getElementById("searchCast").classList.remove("active")
    // appendData(default_list, 0);
    appendData(movie_obj, 0);
})
document.getElementById("searchGenres").addEventListener("click", function () {
    var inputText = document.getElementById("movieSearch");
    inputText.value = "";
    inputText.setAttribute("placeholder", "Genres")
    search_by = "genres";
    this.classList.add('active')
    document.getElementById("searchYear").classList.remove("active")
    document.getElementById("searchTitle").classList.remove("active")
    document.getElementById("searchCast").classList.remove("active")
    // appendData(default_list, 0);
    appendData(movie_obj, 0);
})
document.getElementById("searchCast").addEventListener("click", function () {
    var inputText = document.getElementById("movieSearch");
    inputText.value = "";
    inputText.setAttribute("placeholder", "Cast")
    search_by = "cast";
    this.classList.add('active')
    document.getElementById("searchYear").classList.remove("active")
    document.getElementById("searchGenres").classList.remove("active")
    document.getElementById("searchTitle").classList.remove("active")
    // appendData(default_list, 0);
    appendData(movie_obj, 0);
})




document.getElementById("searchButton").addEventListener("click", function () {
    var search_val = document.getElementById("movieSearch").value;
    if (search_by == 'title') {
        if (search_val) {
            var filtered_movies = movie_obj.filter(function (v) {
                return v.title.toLowerCase().indexOf(search_val.toLowerCase()) !== -1;
            });
            // Send to Python
            // console.log(filtered_movies)
            sendFilteredList(filtered_movies)
            // console.log("Filtered Movies Sent")

            // Send Search Text to Flask
            sendSearchText(filtered_movies, search_by)

            appendData(filtered_movies, 0)
        }
    }
    else if (search_by == 'year') {
        search_year = parseInt(search_val)
        if (search_val) {
            var filtered_movies = movie_obj.filter(function (v) {
                return v.year === search_year
            });

            // Send Search Text to Flask
            sendSearchText(filtered_movies, search_by)

            appendData(filtered_movies, 0)
        }
    }
    //  Could not get this working in time
    else if (search_by == 'genres') {

        // console.log(search_val)
        // console.log(movie_obj)
        if (search_val) {
            var filtered_movies = movie_obj.filter(function (v) {
                if (!v.genres) { return false; }
                // console.log(v.genres)

                var search_val_exists = v.genres.filter(function (entry) {
                    return entry.toLowerCase() === search_val.toLowerCase();
                }).length > 0 ? true : false;
                return search_val_exists;
            });

            sendFilteredList(filtered_movies)

            // Send Search Text to Flask
            sendSearchText(filtered_movies, search_by)

            // console.log("Filtered List: " + filtered_movies);
            appendData(filtered_movies, 0)
        }
    }

    else if (search_by == 'cast') {
        // console.log(search_val)
        // console.log(movie_obj)
        if (search_val) {
            var filtered_movies = movie_obj.filter(function (v) {
                if (!v.cast) { return false; }
                // console.log(v.cast)

                var search_val_exists = v.cast.filter(function (entry) {
                    return entry.toLowerCase() === search_val.toLowerCase();
                }).length > 0 ? true : false;
                return search_val_exists;
            });

            // Send Search Text to Flask
            sendSearchText(filtered_movies, search_by)

            // console.log("Filtered List: " + filtered_movies);
            appendData(filtered_movies, 0)
        }
    }
    //Send Search Field data to /Search-Text Route
})

// Send Filtered List from Search to Flask
function sendFilteredList(list) {
    // console.log(list)
    list_json = JSON.stringify(list)
    // console.log(list_json);
    const URL = '/filtered-list'
    const xhr = new XMLHttpRequest();
    sender = list_json

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(list));
}


// Send Search Text to Flask
function sendSearchText() {
    searchText = document.getElementById('movieSearch').value
    // console.log(searchText);

    const URL = '/search'
    const xhr = new XMLHttpRequest();
    sender = JSON.stringify({ value: searchText })

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(sender);

}


// Search by Title as User Types any letter in the Search Bar(when search_by is set to Title)
// document.getElementById("movieSearch").addEventListener("keyup", function (e) {
//     if (search_by == 'title') {
//         var search_val = this.value;
//         if (search_val) {
//             var filtered_movies = movie_obj.filter(function (v) {
//                 return v.title.toLowerCase().indexOf(search_val.toLowerCase()) !== -1;
//             });

//             appendData(filtered_movies, 0)
//         }
//     }
// });

// When Search Box is cleared, Display default List View 
document.getElementById("movieSearch").addEventListener("input", function (e) {
    if (this.value == '') {
        appendData(movie_obj, 0)
    }
});




// ------------ SORT DROPDOWN

var dropDownText = document.getElementById("navbarDropdown");

// --- SORT BY TITLE
// 
document.getElementById("sortByTitle").addEventListener("click", function () {
    dropDownText.innerHTML = "Title ";
    var listByTitle = movie_obj.sort((a, b) => a.title.localeCompare(b.title))
    appendData(listByTitle, 0)
})


// --- SORT BY YEAR

// Descending: newest to oldest
document.getElementById("soryByYearNew").addEventListener("click", function () {
    dropDownText.innerHTML = "Newest ";
    var movieLstNew = movie_obj.sort((a, b) => b.year - a.year);
    appendData(movieLstNew, 0)
})

// Accending: oldest to newest
document.getElementById("soryByYearOld").addEventListener("click", function () {
    dropDownText.innerHTML = "Oldest ";
    var movieLstOld = movie_obj.sort((a, b) => a.year - b.year);
    appendData(movieLstOld, 0)
})


// Seperate Fetch for Default List that will not be changed
// Used for reload of list with Reset Button

// var default_list;
// fetch('./static/movies.json')
//     .then(function (response) {
//         return response.json();
//     })
//     .then(function (data) {
//         appendData(data, 0);
//         default_list = data;
//     })
//     .catch(function (err) {
//         console.log('error: ' + err);
//     });


// --- RESET 
//     SET LIST BACK TO DEFAULT VIEW, Clear Radio buttons, Reset Drop Down text, reset Searc Text Placeholder
document.getElementById("resetListSort").addEventListener("click", function () {
    restAll()
})

function restAll() {
    dropDownText.innerHTML = "Sort By "
    document.getElementById("radio10").checked = false;
    document.getElementById("radio20").checked = false;
    document.getElementById("radio30").checked = false;
    document.getElementById("movieSearch").value = '';
    document.getElementById("movieSearch").setAttribute("placeholder", "Title")
    document.getElementById("searchYear").classList.remove("active")
    document.getElementById("searchGenres").classList.remove("active")
    document.getElementById("searchTitle").classList.remove("active")
    document.getElementById("searchCast").classList.remove("active")
    search_by = "title";
    per_page = 5;
    appendData(movie_obj, 0)
}





// ------------  RADIO NUMBER PER PAGE

document.getElementById("radio10").addEventListener("click", function () {
    per_page = 10;
    appendData(movie_obj, 0)
})
document.getElementById("radio20").addEventListener("click", function () {
    per_page = 20;
    appendData(movie_obj, 0)
})
document.getElementById("radio30").addEventListener("click", function () {
    per_page = 30;
    appendData(movie_obj, 0)
})




// ------------ PREVIOUS AND NEXT PAGE
// Use an index to set where the list should start, it sarts at 9, and adds per page
// to base to get the index of the nth element to display
// First 0, if per_page set to 20, then next page will start at 21 to 40, etc. 
var j = 0;
document.getElementById("prevPage").addEventListener("click", function () {
    document.getElementById("search_results").innerHTML = "";
    if (j > 0) {
        j = j - 1;
    }
    var a = j * per_page;
    appendData(movie_obj, a);
})

document.getElementById("nextPage").addEventListener("click", function () {
    document.getElementById("search_results").innerHTML = "";
    j = j + 1;
    var a = j * per_page;
    appendData(movie_obj, a);
})



//Send Title of Movie Clicked to Backend
function getMovieData(btn) {

    title = btn.innerHTML;
    // console.log(title);

    const URL = '/viewed_movie'
    const xhr = new XMLHttpRequest();
    sender = title

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: title
    }));
    // alert("Movie added to Viewed List")
}


// Send list of Shown movies on the page to backend
function sendShownList(obj) {

    const URL = '/shown_movies'
    const xhr = new XMLHttpRequest();
    sender = JSON.stringify(obj)

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(sender);

}



// APPEND DATA TO PAGE

function appendData(filtered_movies, b) {

    var frag = document.createDocumentFragment();
    var container = document.getElementById("search_results");
    container.innerHTML = '';
    var objList = [];

    for (var i = b; i < b + per_page; i++) {

        obj = {
            title: filtered_movies[i].title,
            year: filtered_movies[i].year,
            cast: filtered_movies[i].cast,
            genres: filtered_movies[i].genres,
        }

        JSON.stringify(obj)
        // console.log(obj)
        objList.push(obj)


        // var dataHold = document.createElement('span');
        // dataHold.classList.add()
        // dataHold.setAttribute("id", `hidden${i}`)
        // dataHold.setAttribute("hidden", "true")
        // dataHold.innerText = "This is a String"

        var btnEle = document.createElement("button");
        btnEle.setAttribute("type", "button");
        btnEle.classList.add("btn", "shadow", "btn-block", "btn-lg", "movieButton");
        btnEle.setAttribute('name', 'movie_title')
        btnEle.setAttribute("data-toggle", "collapse");
        btnEle.setAttribute("id", "movieButton");
        btnEle.setAttribute("data-target", `#collapseData${i}`);
        btnEle.setAttribute("aria-expanded", "false");
        btnEle.setAttribute("aria-controls", `collapseData${i}`);
        btnEle.setAttribute("ondblclick", "getMovieData(this)")
        btnEle.innerHTML = filtered_movies[i].title;

        var cardEle = document.createElement("div");
        cardEle.classList.add("collapse", "mx-5", "mb-3", "cardData");
        cardEle.setAttribute("id", `collapseData${i}`)
        var cardBody = document.createElement("div");
        cardBody.setAttribute("id", "cardBody")
        cardBody.classList.add("card", "card-body", "movieInfoCard");
        var p = document.createElement("p");
        p.classList.add("card-text");
        var year = document.createElement("span");
        year.innerHTML = `<span>Year: ${filtered_movies[i].year}</span><br>`;
        var genre = document.createElement("span");
        genre.innerHTML = `<span>Genre: ${filtered_movies[i].genres} </span><br>`;
        var cast = document.createElement("span");
        cast.innerHTML = `<span>Cast: ${filtered_movies[i].cast} </span><br>`;


        p.appendChild(year);
        p.appendChild(genre);
        p.appendChild(cast);

        cardBody.appendChild(p);
        cardEle.appendChild(cardBody);

        frag.appendChild(btnEle);
        frag.appendChild(cardEle);

        container.appendChild(frag);
    }

    // console.log(objList)
    sendShownList(objList)
}
















//Send Title of Movie Clicked to Backend
function getTicketNum(btn) {

    task_num = btn.innerHTML;
    // console.log(title);

    const URL = '/task'
    const xhr = new XMLHttpRequest();
    sender = task_num

    xhr.open('POST', URL);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        value: task_num
    }));
    // alert("Movie added to Viewed List")
}