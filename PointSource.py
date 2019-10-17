__author__ = 'Julieanna Bacon'

import numpy as np
from io import StringIO
from astropy.io import ascii

#### L IS LONGITUDE AND THUS IS THE X COMPONENT OF THE GALACTIC COORDINATES ####
#### B IS LATITUDE AND THUS IS THE Y COMPONENT OF THE GALACTIC COORDINATES ####

def SearchRegion(location_ra, location_dec, horzAxis, verAxis = 0, mag = 'null', angle = 'null', ):
    #### Input x - component first, then y - component, then the axes #### angle in radian
    #### mag is the name of the magnitude that the user would like to search by. For example, mag8_0 or mag_j
    #### lowestIntensity is the minimum amount of intensity we want a star to have within the given magnitude

    # Given a location and axes, this will return the pointsource objects that are within that region. Later, this
    # function will write a txt file of the pointsource objects that fit the description and then return it for the user
    #
    # Using minorAxis = 0 in the constructor gives the user the option to search using a circle and not have to specify
    # another axis
    #
    # so if they didn't specify a minorAxis, then we're going to set the minorAxis to distance, which will be the radius
    # of our circle. If we are searching using an ellipse, this section of the code isn't touched.
    if verAxis == 0:
        verAxis = horzAxis

    # List of sources that are within our region. As we find them, we'll append sources to this list and then return it
    regionSources = []

    if mag == 'null':
        for x in sources.getFile():
            # This is the equation for an ellipse
            if angle == 'null':
                ellipseVer = location_dec - x.dec
                ellipseHorz = location_ra - x.ra

            else:
                ellipseVer = (location_ra - x.ra)*np.cos(angle) + (location_dec - x.dec)*np.sin(angle)
                ellipseHorz = (location_ra - x.ra)*np.sin(angle) - (location_dec - x.dec)*np.cos(angle)

            ellipEq = (ellipseVer**2)/float(verAxis**2) + (ellipseHorz)**2/float(horzAxis**2)

            # If our expression is less than or equal to one, then this point source is within the bounds of our ellipse
            if ellipEq <= 1:
                regionSources.append(x)

    elif not mag == 'null':
        for x in sources.getFile():
            # This is the equation for an ellipse
            if angle == 'null':
                ellipseVer = location_dec - x.dec
                ellipseHorz = location_ra - x.ra

            else:
                ellipseVer = (location_ra - x.ra)*np.cos(angle) + (location_dec - x.dec)*np.sin(angle)
                ellipseHorz = (location_ra - x.ra)*np.sin(angle) - (location_dec - x.dec)*np.cos(angle)

            ellipEq = (ellipseVer**2)/float(verAxis**2) + (ellipseHorz)**2/float(horzAxis**2)

            # If our expression is less than or equal to one, then this point source is within the bounds of our ellipse
            if ellipEq <= 1 and not getattr(x,mag) == 'null':
                regionSources.append(x)

    return regionSources


def printRegionSourcesL(regionSources):
    # Input must be a list of objects, aka, the list of sources that satisfy the requirements in SearchRegion
    # Outputs the l component (x - component) of the sources within our region
    arr = []
    for x in regionSources:
        arr.append(x.l)
    print( arr)

def printRegionSourcesB(regionSources):
    # Input must be a list of objects, aka, the list of sources that satisfy the requirements in SearchRegion
    # Outputs the b component (y - component) of the sources within our region
    arr = []
    for x in regionSources:
        arr.append(x.b)
    print( arr)

def printRegionSources(regionSources):
    # Input must be a list of objects, aka, the list of sources that satisfy the requirements in SearchRegion
    # Outputs the b component (y - component) of the sources within our region
    f = open('8mag.txt','a')
    arr = []
    for x in regionSources:
        arr.append(x.mag8_0)
        print >> f,x.ra,x.dec,x.mag8_0        
    print( arr)
    print "This is the number of sources with mag8_0 values: ", len(arr)
    f.close()


class fileList:
    def __init__(self, filename):
        # self.data is a Table object specific to the astropy library. Look at the library for more documentation for
        # how a Table object operates, but it is similar to a 2D array, except with formatting
        self.data = ascii.read(filename)

        # self.file is the list of all of the pointsource objects we've created
        self.file = self.createFileList()

    def getFile(self):
        return self.file

    def printFile(self, string):
        for x in string:
            print (x)

    def createFileList(self):
        pointsources = []

        # from the glimpse catalog, these are the headers for each column in our Table
        headers = ['designation','l','b','ra','dec','dra','ddec','csf','mag_j','dj_m','mag_h','dh_m','mag_ks','dks_m',
                   'mag3_6','d3_6m','mag4_5','d4_5m','mag5_8','d5_8m','mag8_0','d8_0m','f_j','df_j','f_h','df_h','f_ks',
                   'df_ks','f3_6','df3_6','f4_5','df4_5','f5_8','df5_8','f8_0','df8_0','color36_45','color36_58',
                   'color36_80','color45_58','color45_80','color58_80']

        # so range(len(self.data['designation'])) is creating an array from 0 to the number of sources that we have in
        # our file. for y in that array means that it will execute the below for each element of the array, meaning that
        # will do the below for each source in our original txt file.
        for y in xrange(len(self.data['designation'])):

            #this notation is specific to the astropy table, so I would recommend looking at that documentation if you're
            # confused, but self.data is an astropy table, and self.data[name of a column] will give you a new table
            # object with only one column, which is the column you specified.
            # So self.data['designation'] will give you all of the names of all of the pointsources in the orginal file
            designation = self.data[headers[0]][y]
            l = self.data[headers[1]][y]
            b = self.data[headers[2]][y]
            ra = self.data[headers[3]][y]
            dec = self.data[headers[4]][y]
            dra = self.data[headers[5]][y]
            ddec = self.data[headers[6]][y]
            csf = self.data[headers[7]][y]
            mag_j = self.data[headers[8]][y]
            dj_m  = self.data[headers[9]][y]
            mag_h = self.data[headers[10]][y]
            dh_m = self.data[headers[11]][y]
            mag_ks = self.data[headers[12]][y]
            dks_m = self.data[headers[13]][y]
            mag3_6 = self.data[headers[14]][y]
            d3_6m = self.data[headers[15]][y]
            mag4_5 = self.data[headers[16]][y]
            d4_5m = self.data[headers[17]][y]
            mag5_8 = self.data[headers[18]][y]
            d5_8m = self.data[headers[19]][y]
            mag8_0 = self.data[headers[20]][y]
            d8_0m = self.data[headers[21]][y]
            f_j  = self.data[headers[22]][y]
            df_j = self.data[headers[23]][y]
            f_h  = self.data[headers[24]][y]
            df_h = self.data[headers[25]][y]
            f_ks = self.data[headers[26]][y]
            df_ks = self.data[headers[27]][y]
            f3_6 = self.data[headers[28]][y]
            df3_6 = self.data[headers[29]][y]
            f4_5 = self.data[headers[30]][y]
            df4_5  = self.data[headers[31]][y]
            f5_8  = self.data[headers[32]][y]
            df5_8  = self.data[headers[33]][y]
            color36_45 = self.data[headers[34]][y]
            color36_58  = self.data[headers[35]][y]
            color36_80  = self.data[headers[36]][y]
            color45_58  = self.data[headers[37]][y]
            color45_80  = self.data[headers[38]][y]
            color58_80  = self.data[headers[39]][y]


            # creating a new point source object with all of the attributes we pulled from
            pointsource = PointSource(designation,l,b,ra,dec,dra,ddec,csf,mag_j,dj_m,mag_h,dh_m,mag_ks,dks_m,
                                      mag3_6,d3_6m,mag4_5,d4_5m,mag5_8,d5_8m,mag8_0,d8_0m,f_j,df_j,f_h,df_h,f_ks,df_ks,
                                      f3_6, df3_6,f4_5,df4_5,f5_8,df5_8,color36_45,color36_58,color36_80,color45_58,
                                      color45_80, color58_80)
            pointsources.append(pointsource)
        return pointsources



class PointSource:
    # This has an absurdly long constructor, and I'll eventually make it nicer looking later on, but for now it works.
    def __init__(self, designation, l, b, ra,dec,dra,ddec,csf,mag_j,dj_m,mag_h,dh_m,mag_ks,dks_m,
                    mag3_6,d3_6m,mag4_5,d4_5m,mag5_8,d5_8m,mag8_0,d8_0m,f_j,df_j,f_h,df_h,f_ks,df_ks, f3_6, df3_6,
                    f4_5,df4_5,f5_8,df5_8,color36_45,color36_58,color36_80,color45_58, color45_80, color58_80):

        #this is the name of the pointsource
        self.designation = designation
        # l is the longitude part of the galactic coordinates
        self.l = l

        # b is the latitude part of the galactic coordinates
        self.b = b

        # not 100% what each of these variables actually are, but they're the column headers on the sources file, so I'm
        # sure the glimpse catalog has an explanation of what each one physically means.
        self.ra = ra
        self.dec = dec
        self.dra = dra
        self.ddec = ddec
        self.csf = csf
        self.mag_j = mag_j
        self.dj_m = dj_m
        self.mag_h = mag_h
        self.dh_m = dh_m
        self.mag_ks = mag_ks
        self.dks_m = dks_m
        self.mag3_6 = mag3_6
        self.d3_6m = d3_6m
        self.mag4_5 = mag4_5
        self.d4_5m = d4_5m
        self.mag5_8 = mag5_8
        self.d5_8m = d5_8m
        self.mag8_0 = mag8_0
        self.d8_0m = d8_0m
        self.f_j = f_j
        self.df_j = df_j
        self.f_h = f_h
        self.df_h = df_h
        self.f_ks = f_ks
        self.df_ks = df_ks
        self.f3_6 = f3_6
        self.df3_6 =df3_6
        self.f4_5 = f4_5
        self.df4_5 = df4_5
        self.f5_8 = f5_8
        self.df5_8 = df5_8
        self.color36_45 = color36_45
        self.color36_58 = color36_58
        self.color36_80 = color36_80
        self.color45_58 = color45_58
        self.color45_80 = color45_80
        self.color58_80 = color58_80

        # sets the cloud that our point source is in, currently the default is cloud C. output is "C"
        self.cloud = self.setCloud()


    def getLocation(self):
        # returns the galactic coordinates in the same format that the glimpse catalog
        # requires the input location
        return self.l + " " + self.b + " ga"

    def getL(self):
        #returns the longitude componet of the galactic coordinates
        return self.l

    def getB(self):
        # returns the latitude component of the galatic coordinates
        return self.b

    def getCloud(self):
        return self.cloud

    def setCloud(self):
        # This is the default for now. When we're using more than one cloud, it'll be pretty easy to go through the list
        # of pointsources we have to see which ones are inside each cloud and then assign them to that cloud, much like
        # our search region function
        self.cloud = "C"


class Cloud:
    def __init__(self):
        # so far this just has an array of all of the pointsource objects.
        self.stars = sources.getFile()


if __name__ == "__main__":
    # Put code that you want the program to run here

    # This creates a new instance of
    sources = fileList("FormattedCloudCSources.txt")
    cloudC = Cloud()
    radius = 27./3600.
    targets = ['C2','C6','C9','B1','B2','H6']
    contin = {'C2':[280.70956,-4.0556528],'C9':[280.716644411, -3.99837805537],'C6':[280.725266243, -4.04095388787],'B1':[276.466902044, -12.081236648],'B2':[276.495809604, -12.0707316512],'H5':[284.286070595, 2.15040694357],'H6':[284.285449644, 2.18149861044]}
    for target in targets:
        center_ra = contin[target][0]
        center_dec = contin[target][1]
        print target
        printRegionSources(SearchRegion(center_ra, center_dec, radius, 0, 'mag8_0'))
    #(printRegionSources8Mag(SearchRegion(28.373, .076, .1025,0.075, 'mag8_0')))
