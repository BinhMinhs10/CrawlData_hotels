# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# Preprocessing data or clearning data
# mytour.vn
def isNaN(num):
    return num != num
def preprocess_star_booking(star):
    if isNaN(star):
        return 0
    import re
    number = re.findall('\d',str(star) )
    return number[0]

def preprocess_price_booking(price):
    price = price[4:]
    price = price.replace('.', '')
    return price.strip()
# ===================================================================
def preprocess_title(title):
    title = title.lower()
    title = title.replace('khách sạn','')
    title = title.replace(',', ' ')
    title = title.replace("'", '')
    title = title.replace('&', 'and')
    title = title.replace('?', '')
    return title.strip()

def preprocess_star(star):
    star = str(star)
    star = star.replace(',', '.')
    star = star[:-3]
    return star.strip()
def preprocess_rooms_hotels(rooms):
    import ast
    rooms = ast.literal_eval(rooms)
    return rooms
def preprocess_price_hotels(price):
    price = price[:-1]
    price = price.replace('.', '')
    return price.strip()
def preprocess_images(image):
    import ast
    pdict = ast.literal_eval(image)    
    pdict[0]['path'] = 'images/'+ pdict[0]['path']
    pdict = pdict[0]
    return pdict
def preprocess_address(address):
    address = address.split(',')[0]
    return address

# ===================================================================
def prep_price_ivivu(price):
    price = price.replace('.', '')
    price = price.replace('VND', '')
    return price.strip()
def preprocess_rooms_ivivu(rooms):
    if isNaN(rooms):
        pass
    else:
        import ast
        rooms = ast.literal_eval(rooms) 
        for room in rooms:
            room['price_per_night'] = prep_price_ivivu(room['price_per_night'])
    return rooms
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=+
# ++++++++++++++++++++++++++++++++++++++++++++++++===

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++===
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=+
    
# Load data Booking.com
booking = pd.read_csv('./booking.csv')

booking['norm_image'] = booking['images'].map(preprocess_images)
booking['norm_name'] = booking['name'].map(preprocess_title)
booking['head_address'] = booking['address'].map(preprocess_address)
booking['norm_address'] = booking['address'].map(preprocess_title)
booking['norm_star'] = booking['star'].map(preprocess_star_booking) 
booking['norm_star'] = booking['norm_star'].astype(int)   

booking['rooms'] = booking['rooms'].map(preprocess_rooms_hotels)
# preprocessing price
for rooms in booking['rooms']:
    for room in rooms:
        room['price_per_night'] = preprocess_price_booking(room['price_per_night'])
        
booking = booking.drop(['images','star'], axis=1)

# ++++++++++++++++++++++++++++++++++++++++++++++++===
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=+


# load data from hotels.com
hotels = pd.read_csv('./hotels.csv')

# phai chay lan luot tung dong o tren
hotels['norm_name'] = hotels['name'].map(preprocess_title)
hotels['head_address'] = hotels['address'].map(preprocess_address)
hotels['norm_address'] = hotels['address'].map(preprocess_title)
hotels['norm_image'] = ''

# Preprocessing rooms
hotels['rooms'] = hotels['rooms'].map(preprocess_rooms_hotels)
# preprocessing price
for rooms in hotels['rooms']:
    for room in rooms:
        room['price_per_night'] = preprocess_price_hotels(room['price_per_night'])
        
hotels['norm_star'] = hotels['star'].map(preprocess_star)
hotels['norm_star'].astype(str)
hotels = hotels.drop(['images','star'], axis=1)
#hotels.to_csv('normed_hotels.csv')

# ++++++++++++++++++++++++++++++++++++++++++++++++===
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++===

# load data from ivivu.com
ivivus = pd.read_csv('./ivivu.csv')

# phai chay lan luot tung dong o tren
ivivus['norm_name'] = ivivus['name'].map(preprocess_title)
ivivus['head_address'] = ivivus['address'].map(preprocess_address)
ivivus['norm_address'] = ivivus['address'].map(preprocess_title)
ivivus['rooms'] = ivivus['rooms'].map(preprocess_rooms_ivivu)
ivivus['norm_star'] = ''    
ivivus['norm_image'] = ''
ivivus = ivivus.drop(['images','star'], axis=1)


hotels = hotels.drop_duplicates(subset=['norm_name', 'norm_address'], keep='first').copy()
booking = booking.drop_duplicates(subset=['norm_name','norm_address'], keep='first').copy()
ivivus = ivivus.drop_duplicates(subset=['norm_name','norm_address'], keep='first').copy()

hotels = hotels.reset_index()
booking = booking.reset_index()
ivivus = ivivus.reset_index()

import py_stringsimjoin as ssj
import py_stringmatching as sm
#
hotels['id'] = range(hotels.shape[0])
booking['id'] = range(booking.shape[0])
ivivus['id'] = range(ivivus.shape[0])

# Edit distance
#similar_titles = ssj.edit_distance_join(hotels, mytour , 'id', 'id', 'norm_name','norm_name', l_out_attrs=['link','norm_name','norm_address','rooms', 'norm_star', 'benefits','norm_image'], r_out_attrs=['link','norm_name','norm_address','rooms', 'norm_star', 'benefits','norm_image'], threshold=2)


# A: Finding a candidate set using simple heuristic
# create mixture column
ssj.utils.converter.dataframe_column_to_str(booking, 'norm_star', inplace=True)
booking['mixture'] = booking['norm_name'] + ' ' + booking['norm_address']

# repeating the same thing for the kaggle db
#ssj.utils.converter.dataframe_column_to_str(hotels, 'norm_star', inplace=True)
hotels['mixture'] = hotels['norm_name'] + ' ' + hotels['norm_address'] 

C = ssj.overlap_coefficient_join(hotels, booking, 'id','id', 'mixture', 'mixture', sm.WhitespaceTokenizer(), 
                                 l_out_attrs=['link','norm_name','name','norm_address','head_address','rooms', 'norm_star', 'benefits','norm_image','rating','destination'], 
                                 r_out_attrs=['link','norm_name','name','norm_address','head_address','rooms', 'norm_star', 'benefits','norm_image','rating','destination'], 
                                 threshold=0.7)
print(C.shape)


# Creating the Rule-Based Matcher
import py_entitymatching as em
em.set_key(hotels, 'id')
em.set_key(booking, 'id')
em.set_key(C, '_id')
em.set_ltable(C, hotels)
em.set_rtable(C, booking)
em.set_fk_rtable(C, 'r_id')
em.set_fk_ltable(C, 'l_id')

brm = em.BooleanRuleMatcher()

booking.dtypes
# Generate a set of features
F = em.get_features_for_matching(hotels, booking, validate_inferred_attr_types=False)
F.feature_name


#row = 45
#lev.get_sim_score(C.iloc[[row]]['l_norm_name'][row],C.iloc[[row]]['r_norm_name'][row])

# excute sim score
#C['pred_label']=0
#for row in range(C.shape[0]):
#    t = lev.get_sim_score(C.iloc[[row]]['l_norm_name'][row],C.iloc[[row]]['r_norm_name'][row])
#    if t > 0.5:    
#        C['pred_label'][row] = 1
#C = C.loc[C['pred_label'] == 1]
    

# Add two rules to the rule-based matcher
# The first rule has two predicates, one comparing the titles and the other looking for an exact match of the years
brm.add_rule(['norm_name_norm_name_lev_sim(ltuple, rtuple) > 0.5'], F)

# This second rule compares the authors
#brm.add_rule(['head_address_head_address_lev_sim(ltuple, rtuple) > 0.8'], F)
brm.get_rule_names()

result_match = brm.predict(C, target_attr='pred_label', append=True)
result_match = result_match.loc[result_match['pred_label'] == 1]

# 
# return result to show web app
# ===========================================================================

l_match=list(result_match['l_id'])
hotels = hotels.drop(l_match, axis=0)
 

r_match=list(result_match['r_id'])
booking = booking.drop(r_match, axis=0)

def schema_mapping(hotel, name_source):
    ht={}
    ht['address'] = hotel['address']
    ht['name'] = hotel['name']
    ht['benefits'] = hotel['benefits']
    ht['destination'] = hotel['destination']
    ht['rating'] = hotel['rating']
    if hotel['norm_star'] != '':
        ht['star'] = hotel['norm_star']
    else:
        ht['star'] = ''
    datasets=[]
    
    dataset={}
    dataset['name_source'] =name_source
    dataset['link'] = hotel['link']
    
    if hotel['norm_image'] != '':
        dataset['image'] = hotel['norm_image']['path']
    dataset['rooms'] = hotel['rooms']
    datasets.append(dataset)
    
    ht['datasets'] = datasets
    return ht
def schema_matching(result_match, left, right):
    import math
    ht={}
    if len(result_match['l_norm_address']) > len(result_match['r_norm_address']):
        ht['address'] = result_match['l_norm_address']
    else:
        ht['address'] = result_match['r_norm_address']
        
    if len(result_match['l_norm_name']) > len(result_match['r_norm_name']):
        ht['name'] = result_match['l_name']
    else:
        ht['name'] = result_match['r_name']
    
    if len(str(result_match['l_benefits'])) > len(str(result_match['r_benefits'])):
        ht['benefits'] = result_match['l_benefits']
    else:
        ht['benefits'] = result_match['r_benefits']
    
    if len(result_match['l_destination']) > len(result_match['r_destination']):
        ht['destination'] = result_match['l_destination']
    else:
        ht['destination'] = result_match['r_destination']
    
    
    ht['star'] = result_match['l_norm_star']
    
    
    if math.isnan(result_match['l_rating']):
        ht['rating'] = result_match['r_rating']
    elif math.isnan(result_match['r_rating']):
        ht['rating'] = result_match['l_rating']
    else:
        if result_match['l_rating'] is None:
            ht['rating'] = result_match['r_rating']
        elif int(result_match['l_rating']) > int(result_match['r_rating']):
            ht['rating'] = result_match['l_rating']
        else:
            ht['rating'] = result_match['r_rating']
    datasets=[]
    dataset1={}
    dataset1['name_source'] = left
    dataset1['link'] = result_match['l_link']
    dataset1['image'] = result_match['l_norm_image']
    dataset1['rooms'] = result_match['l_rooms']
    datasets.append(dataset1)
    
    dataset={}
    dataset['name_source'] = right
    dataset['link'] = result_match['r_link']
    dataset['image'] = result_match['r_norm_image']['path']
    dataset['rooms'] = result_match['r_rooms']
    datasets.append(dataset)
    
    ht['datasets'] = datasets
    return ht
    
mediated_schema = []
for index, hotel in hotels.iterrows():
    mediated_schema.append(schema_mapping(hotel, 'hotels'))
# mytour
for index, hotel in booking.iterrows():
    mediated_schema.append(schema_mapping(hotel, 'booking'))

for index, row in result_match.iterrows():
    mediated_schema.append(schema_matching(row,'hotels','booking'))

# add ivivus to mediated schema
df = pd.DataFrame(mediated_schema)   
df['norm_name'] = df['name'].map(preprocess_title)
df['norm_address'] = df['address'].map(preprocess_title)
df['star'] = df['star'].astype(str)
df['id'] = range(df.shape[0])
# A: Finding a candidate set using simple heuristic
# create mixture column
ivivus['mixture'] = ivivus['norm_name'] + ' ' + ivivus['norm_address']

# repeating the same thing for the mediated schema
df['mixture'] = df['norm_name'] + ' ' + df['norm_address']

D = ssj.overlap_coefficient_join(ivivus, df, 'id','id', 'mixture', 'mixture', sm.WhitespaceTokenizer(), 
                                 l_out_attrs=['link','norm_name','name','norm_address','head_address','rooms', 'benefits','rating','destination'], 
                                 r_out_attrs=['datasets','norm_name','name','norm_address','star', 'benefits','rating','destination'], 
                                 threshold=0.7)
print(D.shape)


# Creating the Rule-Based Matcher
import py_entitymatching as em
em.set_key(df, 'id')
em.set_key(ivivus, 'id')
em.set_key(D, '_id')
em.set_ltable(D, ivivus)
em.set_rtable(D, df)
em.set_fk_rtable(D, 'r_id')
em.set_fk_ltable(D, 'l_id')

brm = em.BooleanRuleMatcher()

# Generate a set of features
#F = em.get_features_for_matching(ivivus, df, validate_inferred_attr_types=False)
F.feature_name

# Add two rules to the rule-based matcher
# The first rule has two predicates, one comparing the titles and the other looking for an exact match of the years
brm.add_rule(['norm_name_norm_name_lev_sim(ltuple, rtuple) > 0.5'], F)

# This second rule compares the authors
#brm.add_rule(['head_address_head_address_lev_sim(ltuple, rtuple) > 0.8'], F)
brm.get_rule_names()

result_match_after = brm.predict(D, target_attr='pred_label', append=True)
result_match_after = result_match_after.loc[result_match_after['pred_label'] == 1]

l_match=list(result_match_after['l_id'])
ivivus = ivivus.drop(l_match, axis=0)

for index, hotel in ivivus.iterrows():
    mediated_schema.append(schema_mapping(hotel, 'ivivus.com'))

def map2mediatedchema(result_match, mediated, local):
    ht={}
    if len(result_match['l_norm_address']) > len(result_match['r_norm_address']):
        ht['address'] = result_match['l_norm_address']
    else:
        ht['address'] = result_match['r_norm_address']
        
    if len(result_match['l_norm_name']) > len(result_match['r_norm_name']):
        ht['name'] = result_match['l_name']
    else:
        ht['name'] = result_match['r_name']
    
    if len(str(result_match['l_benefits'])) > len(str(result_match['r_benefits'])):
        ht['benefits'] = result_match['l_benefits']
    else:
        ht['benefits'] = result_match['r_benefits']
    
    if len(result_match['l_destination']) > len(result_match['r_destination']):
        ht['destination'] = result_match['l_destination']
    else:
        ht['destination'] = result_match['r_destination']
    
    
    ht['star'] = result_match['r_star']
    
    
    
    ht['rating'] = result_match['l_rating']
    
    datasets=mediated['datasets']
    dataset1={}
    dataset1['name_source'] = local
    dataset1['link'] = result_match['l_link']
    dataset1['rooms'] = result_match['l_rooms']
    datasets.append(dataset1)
    
    
    ht['datasets'] = datasets
    return ht

for index, row in result_match_after.iterrows():
    mediated_schema[row['r_id']] = map2mediatedchema(row, mediated_schema[row['r_id']], 'ivivu.com')
    

import json
# id about 3000 will have double dataset
with open('dataDDV.json', 'w') as outfile:
    json.dump(mediated_schema, outfile, ensure_ascii=False, indent=4)
