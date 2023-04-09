# Your name: Paul Chafetz
# Your student id: 17039004
# Your email: pchafetz@umich.edu
# List who you have worked with on this homework: N/A

import sqlite3
import unittest

import matplotlib.pyplot as plt


def load_rest_data(db: str) -> dict[str, dict]:
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT name, categories.category, buildings.building, rating FROM restaurants
                JOIN categories ON restaurants.category_id = categories.id
                JOIN buildings ON restaurants.building_id = buildings.id""")
    items = cur.fetchall()
    return {name: {'category': category, 'building': building, 'rating': rating} 
            for name, category, building, rating in items}

def plot_rest_categories(db: str) -> dict[str, int]:
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT categories.category, COUNT(*) FROM restaurants
                JOIN categories ON restaurants.category_id = categories.id
                GROUP BY categories.category
                ORDER BY COUNT(*) ASC""")
    items = cur.fetchall()
    
    ys, xs = zip(*items)
    plt.title("Types of Restaurant on South University Ave")
    plt.xlabel("Number of Restaurants")
    plt.ylabel("Restaurant Categories")
    plt.xticks(list(set(xs)), list(set(xs)))
    plt.barh(ys, xs)
    return {category: count for category, count in items}

def find_rest_in_building(building_num: int, db: str) -> list[str]:
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT name FROM restaurants
                JOIN buildings ON restaurants.building_id = buildings.id
                WHERE buildings.building = ?
                ORDER BY rating DESC""", (building_num, ))
    items = cur.fetchall()
    return [name for name, in items]

#EXTRA CREDIT
def get_highest_rating(db: str) -> list[tuple]:
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("""SELECT categories.category, ROUND(AVG(rating), 1) FROM restaurants
                JOIN categories ON restaurants.category_id = categories.id
                GROUP BY categories.category
                ORDER BY ROUND(AVG(rating), 1) ASC""")
    categories = cur.fetchall()
    cur.execute("""SELECT buildings.building, ROUND(AVG(rating), 1) FROM restaurants
                JOIN buildings ON restaurants.building_id = buildings.id
                GROUP BY buildings.building
                ORDER BY ROUND(AVG(rating), 1) ASC""")
    buildings = cur.fetchall()
    
    cat_ys, cat_xs = zip(*categories)
    bld_ys, bld_xs = zip(*buildings)
    bld_ys_str = [str(bld) for bld in bld_ys]
    plt.figure(figsize=(8, 8))
    plot1 = plt.subplot(2, 1, 1)
    plot2 = plt.subplot(2, 1, 2)

    plot1.set_title("Average Restaurant Ratings by Category")
    plot1.set_xlabel("Ratings")
    plot1.set_ylabel("Categories")
    plot1.barh(cat_ys, cat_xs)
    plot1.set_xlim(0, 5)
    
    plot2.set_title("Average Restaurant Ratings by Building")
    plot2.set_xlabel("Ratings")
    plot2.set_ylabel("Buildings")
    plot2.barh(bld_ys_str, bld_xs)
    plot2.set_xlim(0, 5)
    return [(cat_ys[-1], cat_xs[-1]), (bld_ys[-1], bld_xs[-1])]


def main():
    filename = 'South_U_Restaurants.db'
    building = 1140
    
    rest_data = load_rest_data(filename)
    print('Restaurant data:\n', rest_data)
    
    cat_data = plot_rest_categories(filename)
    print('\nCategory data:\n', cat_data)
    
    rest_list = find_rest_in_building(building, filename)
    print(f'\nRestaurants in building {building}:\n', rest_list)
    
    highest_rating = get_highest_rating(filename)
    print('\nHighest and average ratings:\n', highest_rating)
    plt.show()


class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
