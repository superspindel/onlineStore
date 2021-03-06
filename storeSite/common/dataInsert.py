try:
    from storeSite.database.Database import Database
except:
    from database.Database import Database
try:
    from storeSite.common.product import product
except:
    from common.product import product

try:
    import common.user as user
except:
    import storeSite.common.user as user
import datetime


def insertProducts(categoryID, name, description, price, salePrice, timevariable, prodDate, prodID, prodDateID,
                   quantity):
    mydb = Database()
    table = "Product"
    newProduct = product(prodID, name, description,
                         price, salePrice, 0.0, 0, datetime.date.today(), categoryID)
    mydb.insert(table, newProduct.format())
    i = 0
    while(i<timevariable):
        dateStart = prodDate+' '+str(2*i)+':00:00'
        dateEnd = prodDate+' '+str((2*i)+2)+':00:00'
        mydb.insert("ProductDate", str(prodID)+","+"'"+str(dateStart)+"'"+","+"'"+str(dateEnd)+"'"+","+
                    str(prodDateID+i)+","+str(quantity))
        i += 1
    mydb.end()


def createCategory(categoryID, name):
    mydb = Database()
    table = "categories"
    mydb.insert(table, str(categoryID)+","+"'"+name+"'")
    mydb.end()


def createSubCategory(subCatID, nameList, catID):
    mydb = Database()
    table = "subCategories"
    i = subCatID
    for name in nameList:
        mydb.insert(table, "'"+name+"'"+","+str(catID)+","+str(i))
        i += 1
    mydb.end()


"""
createCategory(1, "Hushåll")
createCategory(2, "Gården")
createCategory(3, "Matlagning")
createCategory(4, "Reparation")
createCategory(5, "Renovering")
createCategory(6, "Flytta")
createCategory(7, "Personliga")
createSubCategory(2, ["Gräsklippning", "Rensa ogräs", "Snöskottning", "Kratta löv", "Vattna blommor",
                  "Grusa uppfart", "Klippa buskar", "Ta ner träd"], 2)
createSubCategory(20, ["Frukost", "Lunch", "Middag", "Catering", "Barverk", "Matkasse", "Matlådor"], 3)
createSubCategory(40, ["Bil", "Inomhus", "Elektronik", "Hus", "Båt"], 4)
createSubCategory(60, ["Tapetsering", "Riva", "Måla", "Golv", "Tak", "Fönster", "Kök", "Toalett"], 5)
createSubCategory(80, ["Flytthjälp", "Flyttstädning", "Hyra"], 6)
createSubCategory(100, ["Promenad", "Barnvakt", "Hundvakt", "Hundpromenad", "Prata"], 7)
createSubCategory(120, ["Städning enskilt rum", "Diskning", "Städning hela huset", "Fönsterputs", "Dammtorkning",
                        "Dammsugning", "Skurning"], 1)

insertProducts(120, "Städa vardagsrum", "Vi kommer och städar erat vardagsrum med allt som det innebär",
               499.99, 449.99, 5, '2016-12-01', 10, 110, 2)
insertProducts(2, "Gräsklippning tomt upp till 1000kvm", "Gräsklippning med gräsklippare och trimmer", 329.99, 299.99,
               3, '2017-05-01', 30, 130, 1)
insertProducts(20, "Frukost på sängen", "Vi kommer vid den bestämda tiden med frukost som ni sedan bara kan ta med till"
                                        " sängen och äta", 199.99, 199.99, 8, '2016-12-15', 50, 150, 3)
insertProducts(40, "Däckbyte", "Vi kommer och byter däck på eran bil till de ni behagar, vi har även med oss verktyg",
               99.99, 99.99, 11, '2016-12-23', 70, 180, 1)
insertProducts(60, "Tapetsering av ett rum", "Våra duktiga tapetserare kommer och tapetserar ett rum, var"
                                             "medveten om att egen tapet behövs",
               999.99, 949.99, 11, '2016-12-29', 90, 240, 2)
insertProducts(80, "Paketering", "Våra medarbeterare kommer och paketerar det ni ska ha med er vid flytten och tar"
                                 "samtidigt med sig skräp som ska slängas",
               699.99, 699.99, 8, '2017-01-03', 110, 340, 3)
insertProducts(100, "Promenad 1km", "Vi kommer och tar med dig ut på en promenad så du får se lite av världen "
                                    "utanför husets trygga väggar och samtidigt ger dig en chans att få prata"
                                    "av dig om det som kan tänkas viktigt", 49.99, 44.99, 6, '2016-06-19', 130, 410, 4)
"""
