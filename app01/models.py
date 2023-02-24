from django.db import models


# Create your models here.
class Client(models.Model):
    """ 客户表 """
    clientno = models.CharField(primary_key=True, max_length=10, verbose_name="客户编号")
    clientname = models.CharField(max_length=15, verbose_name="客户名称", default="")
    clientstreet = models.CharField(max_length=10, verbose_name="客户所在街道", blank=True, null=True)
    clientcity = models.CharField(max_length=10, verbose_name="客户所在城市")
    clientstate = models.CharField(max_length=10, verbose_name="客户所在省(区、市)")
    clientzipcode = models.CharField(max_length=6, verbose_name="邮政编码")
    clienttelno = models.CharField(max_length=11, verbose_name="客户电话", default="")
    clientfaxno = models.CharField(max_length=13, blank=True, null=True, verbose_name="客户传真")
    clientwebaddress = models.CharField(max_length=50, blank=True, null=True, verbose_name="客户网址")
    contactname = models.CharField(max_length=10, verbose_name="联系人姓名")
    contacttelno = models.CharField(max_length=11, verbose_name="联系人电话")
    contactfaxno = models.CharField(max_length=17, verbose_name="联系人传真", blank=True, null=True)
    clientemaliaddress = models.CharField(max_length=20, verbose_name="联系人邮箱", default="", blank=True, null=True)
    # '0000000001', '奇项东', '民族大道', '湖北省', '430074', '18947336207', '010-26737123-888'


class Employee(models.Model):
    """ 职员表 """
    employeeno = models.CharField(primary_key=True, max_length=11, verbose_name="雇员编号")
    titleno = models.CharField(max_length=10, verbose_name="职称编号", unique=True)
    title_list = (
        (1, "董事长"),
        (2, "总裁"),
        (3, "总经理"),
        (4, "大区经理"),
        (5, "经理"),
        (6, "高级技工"),
        (7, "普通技工"),
    )
    title = models.IntegerField(verbose_name="职称", choices=title_list)
    firstname = models.CharField(max_length=10, verbose_name="名字")
    # middlename = models.CharField(max_length=10, blank=True, null=True, verbose_name="中间名")
    # lastname = models.CharField(max_length=10, verbose_name="姓氏")
    address = models.CharField(max_length=30, verbose_name="住址")
    worktelno = models.CharField(max_length=11, verbose_name="工作联系方式")
    hometelno = models.CharField(max_length=11, blank=True, null=True, verbose_name="家庭联系方式")
    empemailaddress = models.CharField(max_length=20, verbose_name="邮箱")
    socialscuritynumber = models.CharField(max_length=19, verbose_name="身份证号")
    dob = models.DateField(verbose_name="出生日期")
    position = models.CharField(max_length=5, blank=True, null=True, verbose_name="所在地")
    sex_list = (
        (1, "男"),
        (2, "女")
    )
    sex = models.IntegerField(verbose_name="性别", choices=sex_list)
    salary = models.DecimalField(verbose_name="薪资", max_digits=10, decimal_places=2, default=0)
    datestarted = models.DateField(verbose_name="入职时间")
    outletno = models.ForeignKey('Outlet', models.DO_NOTHING, verbose_name="门店编号", default="")

    class Meta:
        unique_together = (('employeeno', 'titleno'),)


class Faultreport(models.Model):
    """ 检修表 """
    faultreportno = models.CharField(primary_key=True, max_length=10, verbose_name="检修编号", default="")
    vehlicenseno = models.ForeignKey('Vehicle', models.DO_NOTHING, verbose_name="车辆编号")
    datachecked = models.DateField(db_column='dataChecked', verbose_name="检查日期")
    timechecked = models.TimeField(db_column='timeChecked', blank=True, null=True, verbose_name="检查时间")
    comments = models.CharField(max_length=50, blank=True, null=True, verbose_name="评语")
    employeeno = models.ForeignKey(Employee, models.DO_NOTHING, verbose_name="雇员编号", default="")


class Outlet(models.Model):
    """ 门店表 """
    outletno = models.CharField(primary_key=True, max_length=10, verbose_name="商店编号")
    outletstreet = models.CharField(max_length=50, verbose_name="商店所在街道")
    outletcity = models.CharField(max_length=20, verbose_name="商店所在城市")
    outletstate = models.CharField(max_length=20, verbose_name="商店所在省")
    outletzipcode = models.CharField(max_length=6, verbose_name="邮政编码")
    outlettelno = models.CharField(verbose_name="商店电话", max_length=11, default="")
    outletfaxno = models.CharField(blank=True, null=True, verbose_name="商店传真", max_length=17)


class Rentalagreement(models.Model):
    """ 租凭表 """
    rentalno = models.CharField(primary_key=True, max_length=10, verbose_name="租凭编号")
    datestart = models.DateField(verbose_name="租凭开始日期")
    timestart = models.TimeField(verbose_name="租凭开始时间")
    datereturn = models.DateField(verbose_name="租凭结束日期")
    timereturn = models.TimeField(verbose_name="租凭结束时间")
    mileagebefore = models.IntegerField(verbose_name="租凭前里程数")
    mileageafter = models.IntegerField(verbose_name="租凭后里程数")
    policyno = models.CharField(max_length=12, blank=True, null=True, verbose_name="合同编号")  # ZL－20130315－32
    insurance_choice = (
        (1, "交强险"),
        (2, "商业险")
    )
    insurancecovertype = models.IntegerField(blank=True, null=True, verbose_name="保险种类", choices=insurance_choice)
    insurancepremium = models.IntegerField(blank=True, null=True, verbose_name="保险费")
    clientno = models.ForeignKey(Client, models.DO_NOTHING, verbose_name="客户编号")
    vehlicenseno = models.ForeignKey('Vehicle', models.DO_NOTHING, verbose_name="车辆编号")


class Vehicle(models.Model):
    """ 车辆表 """
    vehlicenseno = models.CharField(primary_key=True, verbose_name="车辆编号", max_length=10, null=False)
    vehiclemake = models.CharField(max_length=20, verbose_name="制车厂")
    vehiclemodle = models.CharField(max_length=20, verbose_name="车型")
    color = models.CharField(max_length=10, verbose_name="颜色")
    nodoors = models.CharField(verbose_name="车牌号", max_length=10)
    capacity = models.SmallIntegerField(verbose_name="车容量")
    hirerate = models.SmallIntegerField(verbose_name="日租金")
    outletno = models.ForeignKey(Outlet, models.DO_NOTHING, verbose_name="门店编号")


class Outletmanager(models.Model):
    """ 店长表 """
    managerno = models.IntegerField(primary_key=True, verbose_name="记录编号")
    outletno = models.ForeignKey(verbose_name="商店编号", to="Outlet", to_field="outletno", on_delete=models.CASCADE)
    titleno = models.ForeignKey(verbose_name="职称编号", to="Employee", to_field="titleno", on_delete=models.CASCADE)
    name = models.CharField(max_length=10, verbose_name="姓名")
