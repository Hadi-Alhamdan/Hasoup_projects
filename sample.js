
const sqlite3 = require('sqlite3').verbose();
let db = new sqlite3.Database('blog.db',(err)=>{
    if (err){
        return console.error(err.message);
    }
    console.log('connected to the blog sqlite database');

});


/*db.run('CREATE TABLE Articles(ArticleID INTEGER PRIMARY KEY, ArticleName TEXT, Author TEXT, Date TEXT)' , function (err){
    if (err){
    return console.log(err.message);
    }
    console.log('Table One Created');
});



db.run('CREATE TABLE Comments(CommentID INTEGER PRIMARY KEY, Name TEXT, Content TEXT, Date TEXT, ArticleID INTEGER, FOREIGN KEY (ArticleID) REFERENCES Articles (ArticleID))' , function (err){
    if (err){
    return console.log(err.message);
    }
    console.log('Table Two Created');
});

*/

/* db.run('INSERT INTO Articles(ArticleID, ArticleName, Author, Date)'+
        'VALUES(1111,"PHP","Ahmad","2019"),'+
        '(2222,"DataBase","Mohamad","2020"),'+
        '(3333,"JavaScript","Hadi","2019"),'+
        '(4444,"PHP","Reem","2020"),'+
        '(5555,"JavaScript","Ola","2020"),'+
        '(6666,"Ruby","Hasan","2019"),'+
        '(7777,"Ruby","Ali","2020"),'+
        '(8888,"PHP","Ahmad","2020"),'+
        '(9999,"Laravel","Ahmad","2019")', function(err){
        if(err){
            return console.log(err.message);
        }
        console.log('Data Inserted to Article Table');
    });


db.run('INSERT INTO Comments(Content, Name,Date, ArticleID)'+
        'VALUES("مرحبًا مقالة رائعة","Ahmad","2019",1111),'+
                           '("شكرًا لك على هذه المقالة","Hadi","2019",2222),'+
                           '("من أروع المقالات التي قرأتها","Hasan","2020",3333),'+
                           '("مقالة رائعة","Fatema","2019",4444),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2019",1111),'+
                           '("مرحبًا مقالة رائعة","Hasan","2019",2222),'+
                           '("مرحبًا مقالة رائعة","Hadi","2019",2222),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2019",1111),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",1111),'+
                           '("مرحبًا مقالة رائعة","Hadi","2020",4444),'+
                           '("مرحبًا مقالة رائعة","Mohamad","2020",2222),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",4444),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2019",1111),'+
                           '("المقال غير جيد يمكن أن يكون أفضل","Ahmad","2020",1111),'+
                           '("مرحبًا مقالة رائعة","Hadi","2020",4444),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",1111),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",2222),'+
                           '("شكرًا لك استاذي على هذا المقال الرائع","Mohamad","2020",5555),'+
                           '("مرحبًا مقالة رائعة","Hadi","2019",1111),'+
                           '("مرحبًا مقالة رائعة من أروع المقالات التي قرأتها","Ahmad","2020",5555),'+
                           '("مرحبًا مقالة رائعة","Mohamad","2020",4444),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2019",2222),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",1111),'+
                           '("مرحبًا مقالة رائعة","Hadi","2020",4444),'+
                           '("مرحبًا مقالة رائعة","Ahmad","2020",5555),'+
                           '("مرحبًا مقالة رائعة","Mohamad","2020",1111),'+
                           '("أرجو زيارة صفحتي والإعجاب بها، يوجد بها الكثير من المنتجات الرائعة","Ali","2019",5555)', function(err){
        if(err){
            return console.log(err.message);
        }
        console.log('Data Inserted to Comments Table');
    }); */



 /* db.all('SELECT * FROM Articles WHERE Date = "2019"', function(err, table){
    if (err) {
       return console.log(err.message); 
    }
    console.log(table);
});


db.all(`SELECT ArticleName, Date,
    (SELECT count (*)
    FROM Comments WHERE Comments.ArticleID = Articles.ArticleID'
    )AS Number FROM Articles`, function(err, table){
    if (err) {
            return console.log(err.message);
        }
        console.log(table);
});

*/

/* db.run('UPDATE Comments SET Content = "من اروع المقالات التي قرائتها، شكرا لك" WHERE CommentID = 3', function(err){
    if(err){
        return console.log(err.message);
    }
    console.log('Data Updated');
});
*/

/* db.run('DELETE FROM Comments WHERE CommentID = 6 ', function(err){
    if(err){
        return console.log(err);
    }
    console.log('DATA Deleted');
});
*/

db.all(`SELECT Name, Content,(SELECT ArticleName FROM Articles WHERE Articles.ArticleID = Comments.ArticleID) AS ArticleName, Date FROM Comments`, function(err, table){
    if(err){
        return console.log(err.message);
    }
    console.log(table);
});


db.close((err)=>{
    if (err){
        return console.error(err.message);
    }

    console.log('close the database connection.');
});
