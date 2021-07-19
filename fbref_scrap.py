from os import name
import selenium
from selenium import webdriver
import re
import pandas

#add comments

def get_rows(div):
    table=div.find_element_by_tag_name('table')
    tbod=table.find_element_by_tag_name("tbody")
    thead=table.find_element_by_tag_name('thead')
    rows=tbod.find_elements_by_tag_name("tr")
    return rows,thead

def get_leagues(driver,leagues):

    url_dict={}
    div_comp=driver.find_element_by_id('div_comps_1_fa_club_league_senior')
    rows,_=get_rows(div_comp)
    
    #get url for all clubs 
    for row in rows:
        try:
            col = row.find_element_by_tag_name("a")
        except:
            
            continue
        if col.text in leagues:
            url_dict[col.text]=col.get_attribute("href")
    return url_dict
def get_szn(driver,leagues,szn="2020-2021"):
    #iterate through league urls and collect team (latest for now)
    latest_szn_url={}
    
    for league in leagues:
        driver.get(leagues[league])
        div_szns=driver.find_element_by_id("div_seasons")
        rows,_=get_rows(div_szns)
        for row in rows:
            try:
                    col = row.find_element_by_tag_name("a")
                    if col.text == szn :
                        latest_szn_url[league]=col.get_attribute("href")
            except:
                continue
    
    return latest_szn_url 

def get_teams(driver,url_szn,filter="all"):
    
    url_teams={}
    for league in url_szn:
        driver.get(url_szn[league])
        divs= driver.find_elements_by_tag_name("div")
        
        for div in divs:
            if re.match("^div_results",div.get_attribute("id")):

                rows,_=get_rows(div)
                for row in rows:
                    col = row.find_element_by_tag_name("a")
                    
                    url_teams[col.text]=col.get_attribute("href")
                break
    #print(url_teams)    
    return url_teams
def get_stat(driver,url_teams,stat="standard"):
    head_write=0
    with open("stats.txt",'w+') as f:
        for teams in url_teams:
            driver.get(url_teams[teams])
            divs= driver.find_elements_by_tag_name("div")
            for div in divs:
                if re.match("^div_stats_standard",div.get_attribute("id")):
                    rows,head=get_rows(div)
                    if head_write==0:
                        f.write("%s\n" %head.text)
                        head_write=1
                    for row in rows:
                        print("writing...")
                        f.write("%s\n" %row.text)
                        
                    
                    
                


if __name__ == "__main__" :

    leagues=["Premier League"]

    driver= webdriver.Chrome() 
    search_url="https://fbref.com/en/comps/" 
    driver.get(search_url)
    url_dict=get_leagues(driver,leagues)
    url_szn=get_szn(driver,url_dict)
    url_teams=get_teams(driver,url_szn)
    get_stat(driver,url_teams)