# ----- CONFIGURE YOUR EDITOR TO USE 4 SPACES PER TAB ----- #
import settings
import sys


def connection():
    ''' User this function to create your connections '''
    import sys
    sys.path.append(settings.MADIS_PATH)
    import madis

    con = madis.functions.Connection('/Users/alexiatopalidou/Desktop/erg/yelp_python/yelp.db')
    
    return con

def classify_review(reviewid):
    
#check for compatible data type 
    try:
        val=str(reviewid)
    except ValueError:
        return [("Error! Insert correct data type.")]
    
    # Create a new connection
    global con
    con=connection()
    
    # Create cursors on the connection
    #alternative: create the desired list after every textwindow, posterms, negterms query
    cur=con.cursor()
    cura=con.cursor()
    curb=con.cursor()
    cur1=con.cursor()
    cur2=con.cursor()
    
    #check for existance of given data inside the yelp.db
    curcheck=con.cursor()
    cur.execute("SELECT var('reviewid',?)",(reviewid,))
    check=curcheck.execute("SELECT review_id from reviews where review_id=?",(val,))
    try:
        ch=check.next()
    except StopIteration:
        return [("Error! Insert valid Review id.",)]
    
    #sql query with textwindow - one for each occasion (terms with 1, 2 or 3 words)
    res=cur.execute("SELECT textwindow(text,0,0,1) from reviews where review_id=var('reviewid');")
    resa=cura.execute("SELECT textwindow(text,0,0,2) from reviews where review_id=var('reviewid');")
    resb=curb.execute("SELECT textwindow(text,0,0,3) from reviews where review_id=var('reviewid');")
    
    #get positive/negative terms
    res1=cur1.execute("SELECT * from posterms;")
    res2=cur2.execute("SELECT * from negterms;")

    #create lists that store a)all reviews terms, b)positive terms and c)negative terms
    k=[]
    for n in res:
        k.append(n)

    for n in resa:
        k.append(n)

    for n in resb:
        k.append(n)

    m=[]
    for z in res1:
        m.append(z)

    o=[]
    for p in res2:
        o.append(p)

    #check if the review is positive or negative
    x=0
    for i in k:
        for j in m:
            if i==j:
                x=x+1

    y=0
    for i in k:
        for j in o:
            if i==j:
                y=y+1           
    
    if x>y:
        rsl='positive'
    elif x<y:
        rsl='negative'
    else:
        rsl='neutral'
    
    #return a list with the results
    res=cur.execute("SELECT b.name, ? from business b, reviews r where r.business_id=b.business_id and r.review_id=?",(rsl, val,))
    
    l=[("business_name","result")]
    for i in res:
        l.append(i)

    return l





def classify_review_plain_sql(reviewid):

    # Create a new connection
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
    
    return [("business_name","result")]

def updatezipcode(business_id,zipcode):

 #check for compatible data type 
    try:
        val=str(business_id)
        val2=int(zipcode)
    except ValueError:
        return [("Error! Insert correct data type.",)]
    
    # Create a new connection
    global con
    con=connection()

    # Create a cursor on the connection
    cur=con.cursor()

    #check for existance of given data inside the yelp.db or allowance of data value
    curcheck=con.cursor()
    cur.execute("select var('business_id',?)", (val,))
    check=curcheck.execute("SELECT business_id from business where business_id=?;",(val,))
    try:
        ch=check.next()
    except StopIteration:
        return [("Error! Insert valid Business Id.",)]
    if val2>99999999999999999999:   #we do not actually need that
        return [("Error! Insert valid Zip code.",)]
    
    #execute main sql query
    res=cur.execute("UPDATE business set zip_code=? where business_id=?;",(val2,val,))

    #return ok or comment that return and de-comment the bottom return for the business_id and the new zip_code
    return [('ok',)]

    #res=cur.execute("SELECT business_id, zip_code from business where business_id=?;",(val,))  
    #l=[("business_id", "zip_code"),]

    #for i in res:
    #   l.append(i)
        
    #return l
    
	
def selectTopNbusinesses(category_id,n):

    #check for compatible data type 
    try:
        val=int(category_id)
        val2=int(n)
    except ValueError:
        return [("Error! Insert correct data type",)]
    
    # Create a new connection
    global con
    con=connection()
    
    # Create a cursor on the connection
    cur=con.cursor()
    
    #check for existance of given data inside the yelp.db
    curcheck=con.cursor()
    cur.execute("SELECT var('category_id',?)", (val,))
    check=curcheck.execute("SELECT category_id from category where category_id=?;",(val,))
    try:
        ch=check.next()
    except StopIteration:
        return [("Error! Insert valid Category Id.",)]
    if val2<0:
        return [("Error! Choose >=0 businesses to return.",)]
    
    #execute main sql query
    res=cur.execute("SELECT b.business_id, count(rpn.positive) from reviews_pos_neg rpn, reviews r, business b, business_category bc, category c where rpn.review_id=r.review_id and r.business_id=b.business_id and b.business_id=bc.business_id and bc.category_id=c.category_id and c.category_id=? group by b.business_id order by count(rpn.positive) desc;",(val,))

    #return a list with the results
    l=[("business_id", "number_of_reviews",)]
    for i in res:
        l.append(i)

    return l[0:val2+1]



def traceUserInfuence(userId,depth):
    # Create a new connection
    con=connection()
    # Create a cursor on the connection
    cur=con.cursor()
    


    return [("user_id",),]
