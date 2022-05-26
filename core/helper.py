import datetime
class DataValid:

    def set_data(self,data,to_today,element,index):
        self.data = data
        self.to_today = to_today
        self.elment=element['name']
        self.index=index
        if (len(self.data.split('-')) != 3):
            print('Invalid data format for ' + self.index + ' ' + self.elment + ' is Invalid valid format is YEAR-MOUNT-DAY')

    def is_valid(self):
        self.valid_year_var = self.valid_year(self.data.split('-')[0])
        self.valid_mount_var = self.valid_mount(self.data.split('-')[1])
        self.valid_day_var = self.valid_day(self.data.split('-')[2])
        return (len(self.data.split('-')) == 3)

    def exep(self,var,var_name):
        try:
            int(var)
        except ValueError:
            print(var_name+' for '+self.index+' '+self.elment+' ('+var+') is Invalid valid format is YEAR-MOUNT-DAY')
            return False
        return True

    def valid_year(self,year):
        if self.exep(year,'Year'):
            x = datetime.datetime.now()
            if self.to_today:
                if int(year)>x.year:
                    print('Var to_today is True for '+self.index+' Year is bigger then year now !')
            return int(year)

    def valid_mount(self,mount):
        if self.exep(mount,'Mount'):
            if int(mount)>12 or int(mount)<0:
                print('Mount for ' + self.index + ' ' + self.elment + ' (' + mount + ') '
                    'is Invalid valid format is YEAR-MOUNT-DAY')
            return int(mount)


    def valid_day(self,day):
        if self.exep(day,'Day'):
            print(self.valid_year_var,self.valid_mount_var,day)
            try:
                if self.valid_year_var is not None and self.valid_mount_var:
                    date = datetime.datetime(int(self.valid_year_var), int(self.valid_mount_var), int(day))
            except ValueError:
                print('day is out of range for month')