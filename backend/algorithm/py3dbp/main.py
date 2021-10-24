from flask.typing import TeardownCallable
from werkzeug.wrappers import response
from .constants import RotationType, Axis
from .auxiliary_methods import intersect, set_to_decimal
from shapely.geometry import Polygon
import numpy as np


DEFAULT_NUMBER_OF_DECIMALS = 3
START_POSITION = [0, 0, 0]


class Item:
    def __init__(self,ID ,name, width, height, depth, weight, type_index, Fitted_items=None):
        self.ID=ID
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.weight = weight
        self.rotation_type = 0
        self.position = START_POSITION
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.type_index=type_index
        self.Fitted_items=Fitted_items
        self.format_numbers(self.number_of_decimals)
        #kate
        self.my_wdh = sorted([self.width, self.height, self.depth], reverse = True)
        self.sort_key =  [self.my_wdh[0]*self.my_wdh[1]*self.my_wdh[2], self.my_wdh[0]*self.my_wdh[1], self.weight, self.ID]
    
    def get_sort_key(self):
        ret = list(self.sort_key)
        return ret

    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.weight = set_to_decimal(self.weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def string(self):
        return f"""
        {self.name}:       
            ID:{self.ID}
            X:{self.width}, 
            Y:{self.height}, 
            Z:{self.depth}, 
            Weight:{self.weight}
            rotation:{self.rotation_type}
            position:{self.position}
        """
        #we have to covert the Decimal object to float so that
        #java packer will be happy
    def getResultDictionary(self):
        #conver position information into float

        if self.Fitted_items!=None:
            return{"ID":self.ID,
            "TypeName":self.name,
            "X":float(self.width),
            "Y":float(self.height),
            "Z":float(self.depth), 
            "Weight":float(self.weight),
            "position_x":float(self.position[0]),
            "position_y":float(self.position[1]),
            "position_z":float(self.position[2]),
            "RotationType":self.rotation_type,
            "TypeIndex":self.type_index,
            "Fitted_items":self.Fitted_items
            }
        else:
            return{"ID":self.ID,
            "TypeName":self.name,
            "X":float(self.width),
            "Y":float(self.height),
            "Z":float(self.depth), 
            "Weight":float(self.weight),
            "position_x":float(self.position[0]),
            "position_y":float(self.position[1]),
            "position_z":float(self.position[2]),
            "RotationType":self.rotation_type,
            "TypeIndex":self.type_index,
            }

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        else:
            dimension = []

        return dimension


    def positions(self):
        b = list([(self.position[0]+self.depth), self.position[1], self.position[2]])
        c = list([(self.position[0]+self.depth), self.position[1]+self.width, self.position[2]])
        d = list([self.position[0], self.position[1]+self.width, self.position[2]])
        e = list([self.position[0], self.position[1]+self.width, self.position[2]+self.height])
        f = list([self.position[0], self.position[1], self.position[2]+self.height])
        g = list([self.position[0]+self.depth, self.position[1], self.position[2]+self.height])
        h = list([self.position[0]+self.depth, self.position[1]+self.width, self.position[2]+self.height])
        corners = list([self.position, b, c, d, e, f, g, h])
        return corners
    def four_xypositions(self):
        x, y, z = self.get_dimension()
        return [self.position[0], self.position[1]+z, self.position[0], self.position[1], self.position[0]+x, self.position[1], self.position[0]+x, self.position[1]+z]

    def rotate(self, rotation_type):
        if(rotation_type==1):
            self.depth, self.height = self.height, self.depth
        elif(rotation_type==2):
            self.depth, self.width = self.width, self.depth
            self.width, self.height = self.height, self.width

    def position(self):
        b = list([self.position[0]+self.depth, self.position[1], self.position[2]])
        c = list([self.position[0]+self.depth, self.position[1]+self.width, self.position[2]])
        d = list([self.position[0], self.position[1]+self.width, self.position[2]])
        e = list([self.position[0], self.position[1]+self.width, self.position[2]+self.height])
        f = list([self.position[0], self.position[1], self.position[2]+self.height])
        g = list([self.position[0]+self.depth, self.position[1], self.position[2]+self.height])
        h = list([self.position[0]+self.depth, self.position[1]+self.width, self.position[2]+self.height])
        corners = list([self.position, b, c, d, e, f, g, h])
        return corners

    def limitation(self, rotation):
        self.rotation_type = rotation
        if self.rotation_type == 0:
            x0 = self.position[0]+self.depth
            y0 = self.position[1]+self.width
            z0 = self.position[2]+self.height
            minmax=list([self.position[0], x0, self.position[1], y0, self.position[2], z0])
        elif self.rotation_type == 1:
            x1 = self.position[0]+self.height
            y1 = self.position[1]+self.width
            z1 = self.position[2]+self.depth
            minmax=list([self.position[0], x1, self.position[1], y1, self.position[2], z1])
        elif self.rotation_type == 2:
            x2 = self.position[0]+self.width
            y2 = self.position[1]+self.height
            z2 = self.position[2]+self.depth
            minmax=list([self.position[0], x2, self.position[1], y2, self.position[2], z2])
        return minmax

class Bin:
    def __init__(self, ID, name, width, height, depth, max_weight, type_index):
        self.ID=ID
        self.name = name
        self.width = width
        self.height = height
        self.depth = depth
        self.max_weight = max_weight
        self.items = []
        self.unfitted_items = []
        self.number_of_decimals = DEFAULT_NUMBER_OF_DECIMALS
        self.type_index=type_index
        #kate
        self.my_wdh = sorted([width, height, depth], reverse = True)
        self.pointer = [0,0,0]
        self.occupied = []

    def optimize_limitation(self):
        if len(self.occupied) <= 1 :
            return
        #else:
            #優化限制式

    def check_in_box(self, item):
        L = item.positions()
        print(L)
        max_x, max_y, max_z = [0, 0, 0]

        for xyz in L:
            x, y, z = xyz
            if x > max_x :
                max_x = x
            if y > max_y :
                max_y = y
            if z > max_z :
                max_z = z
        if max_x > self.width or max_y > self.height or max_z > self.depth :
            return False
        else:
            return True
         

    def check_space_legal(self, item):
        L = item.positions() #找到8個點
        if not self.occupied:
            return True
        print(self.occupied)
        for i in self.occupied:
            x_lim, y_lim, z_lim = i
            for xyz in L:
                x, y, z = xyz
                if x > x_lim[0] and x < x_lim[1] and y > y_lim[0] and y < y_lim[1] and z > z_lim[0] and z < z_lim[1]:
                    return False
        return True

    def check_float(self, item, poly1):
        a = np.array(item.four_xypositions()).reshape(4, 2)
        poly2 = Polygon(a).convex_hull
        if poly1.intersection(poly2).area < poly2.area :
            return True
        else:
            return False


    def format_numbers(self, number_of_decimals):
        self.width = set_to_decimal(self.width, number_of_decimals)
        self.height = set_to_decimal(self.height, number_of_decimals)
        self.depth = set_to_decimal(self.depth, number_of_decimals)
        self.max_weight = set_to_decimal(self.max_weight, number_of_decimals)
        self.number_of_decimals = number_of_decimals

    def get_unfitted_items_as_dict_array(self):
        unFittedItemArray=[]
        for unfitted_item in self.unfitted_items:
            unFittedItemArray.append(unfitted_item.getResultDictionary())
        return unFittedItemArray
        
    def string(self):
        return f"""
            ID:{self.ID},
            TypeName:{self.name},
            X:{float(self.width)}, 
            Y:{float(self.height)}, 
            Z:{float(self.depth)}, 
            Weight_limmit:{float(self.max_weight)}
        """
    def getResultDictionary(self):
        #convet Fitted_items to dictionary(array of dics)
        FittedItemArray=[]
        for fitted_item in self.items:
            FittedItemArray.append(fitted_item.getResultDictionary())
        

        unFittedItemArray=[]
        #convert unfitted_items to array of dictionary
        for unfitted_item in self.unfitted_items:
            unFittedItemArray.append(unfitted_item.getResultDictionary())


        return{
            "ID":self.ID,
            "TypeName":self.name,
            "TypeIndex":self.type_index,
            "X":float(self.width),
            "Y":float(self.height),
            "Z":float(self.depth),
            "Weight_limmit":float(self.max_weight),
            "Fitted_items":FittedItemArray,
            "UnFitted_items":unFittedItemArray,
    }

    def get_volume(self):
        return set_to_decimal(
            self.width * self.height * self.depth, self.number_of_decimals
        )

    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return set_to_decimal(total_weight, self.number_of_decimals)

    def put_item(self, item, pivot, poly1):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        #最好放置角度
        best_rot = -1
        if item.my_wdh == [item.width, item.depth, item.height] :
            best_rot = 0
        elif item.my_wdh == [item.height, item.depth, item.width] :
            best_rot = 1
        elif item.my_wdh == [item.depth, item.width, item.height] :
            best_rot = 2
        elif item.ny_wdh == [item.height, item.width, item.depth] :
            best_rot = 3
        elif item.ny_wdh == [item.width, item.height, item.depth] :
            best_rot = 4
        elif item.my_wdh == [item.depth, item.height, item.width] :
            best_rot = 5

        for i in range(0, len(RotationType.ALL)):
            best_rot_flag = False
            item.rotation_type = i
            dimension = item.get_dimension()

            if pivot[1]:
                if self.check_float(item, poly1):
                    continue

            if (
                self.width < pivot[0] + dimension[0] or
                self.height < pivot[1] + dimension[1] or
                self.depth < pivot[2] + dimension[2] or
                not self.check_space_legal(item) or
                not self.check_in_box(item)
            ):
                continue#超出棧版大小

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                
                #加入限制式
                if i == best_rot :
                    self.occupied.append(item.limitation(i))
                    self.items.append(item)
                else:
                    best_rot_flag = True


            if not fit:
                item.position = valid_item_position

            if best_rot_flag:
                continue
            else:
                return fit

        if not fit:
            item.position = valid_item_position

        if best_rot_flag:
            self.occupied.append(item.limitation(i))
            self.items.append(item)

        return fit

    def put_item_only_2D_rotate(self, item, pivot):
        fit = False
        valid_item_position = item.position
        item.position = pivot

        for i in range(0, len(RotationType.TWO_D)):
            item.rotation_type = RotationType.TWO_D[i]
            dimension = item.get_dimension()

            if pivot[1]:
                if self.check_float(item, poly1):
                    continue            

            if (
                self.width < pivot[0] + dimension[0] or
                self.height < pivot[1] + dimension[1] or
                self.depth < pivot[2] + dimension[2] or
                not check_space_legal(item) or
                not check_in_box(item)
            ):
                continue

            fit = True

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item):
                    fit = False
                    break

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit
                self.occupied.append(item.limitation(i))
                self.items.append(item)

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit



class Packer:
    def __init__(self, TWO_D_MODE=False):
        self.bins = []
        self.items = []
        self.unfit_items = []
        self.total_items = 0
        self.TWO_D_MODE=TWO_D_MODE

    def add_bin(self, bin):
        return self.bins.append(bin)

    def add_item(self, item):
        self.total_items = len(self.items) + 1

        return self.items.append(item)

    def pack_to_bin(self, bin, item):
        fitted = False

        if not bin.items:
            if self.TWO_D_MODE:
                response=bin.put_item_only_2D_rotate(item, START_POSITION, Polygon())
            response = bin.put_item(item, START_POSITION, Polygon())

            if not response:
                bin.unfitted_items.append(item)

            return

        point_list = []
        poly_array = np.array(point_list)
        poly1 = Polygon() #更新這層上面
        this_poly = Polygon() #下面那層
        
        for axis in range(0, 3):
            items_in_bin = bin.items

            if axis == Axis.HEIGHT:
                this_poly = poly1
                point_list = []
                poly_array = np.array(point_list)
                poly1 = Polygon()

            for ib in items_in_bin:
                pivot = [0, 0, 0]
                w, h, d = ib.get_dimension()
                if axis == Axis.WIDTH:
                    pivot = [
                        ib.position[0] + w,
                        ib.position[1],
                        ib.position[2]
                    ]
                elif axis == Axis.HEIGHT:
                    pivot = [
                        ib.position[0],
                        ib.position[1] + h,
                        ib.position[2]
                    ]
                elif axis == Axis.DEPTH:
                    pivot = [
                        ib.position[0],
                        ib.position[1],
                        ib.position[2] + d
                    ]


                if self.TWO_D_MODE:
                    if bin.put_item_only_2D_rotate(item, pivot, this_poly):
                        fitted = True
                        tmp1 = np.array(item.four_xypositions()).reshape(4, 2)
                        if point_list:
                            union_poly1 = np.concatenate((point_list,tmp1))
                            poly1 = MultiPoint(union_poly1).convex_hull
                        else:
                            point_list = item.four_xypositions()
                            poly_array = np.array(item.four_xypositions()).reshape(4, 2)
                            poly1 = Polygon(poly_array).convex_hull
                        break
                else:
                    if bin.put_item(item, pivot, this_poly):
                        fitted = True
                        tmp2 = np.array(item.four_xypositions()).reshape(4, 2)
                        if point_list:
                            union_poly1 = np.concatenate((point_list,tmp2))
                            poly1 = MultiPoint(union_poly1).convex_hull
                        else:
                            point_list = item.four_xypositions()
                            poly_array = np.array(item.four_xypositions()).reshape(4, 2)
                            poly1 = Polygon(poly_array).convex_hull
                        break
            if fitted:
                break

        if not fitted:
            bin.unfitted_items.append(item)

    def pack(
        self, bigger_first=False, distribute_items=False,
        number_of_decimals=DEFAULT_NUMBER_OF_DECIMALS
    ):
        for bin in self.bins:
            bin.format_numbers(number_of_decimals)

        for item in self.items:
            item.format_numbers(number_of_decimals)

        self.bins.sort(
            key=lambda bin: bin.get_volume(), reverse=bigger_first
        )
        """
        self.items.sort(
            key=lambda item: item.get_volume(), reverse=bigger_first
        )
        """
        for bin in self.bins:
            for item in self.items:
                self.pack_to_bin(bin, item)

            if distribute_items:
                for item in bin.items:
                    self.items.remove(item)
    
    #kate
    def sort_items(self):
        self.items.sort(key = lambda s: s.get_sort_key())
