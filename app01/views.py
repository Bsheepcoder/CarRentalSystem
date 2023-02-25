from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
# 从app01中导入model
from app01 import models
from django import forms
from django.core.exceptions import ValidationError
# 引入分页模块
from django.core.paginator import Paginator
from django.http import JsonResponse


# Create your views here.


# def test(request):
#     queryset = models.client.objects.all()
#     return render(request, "test/test.html", {"queryset": queryset})

# 首页
def index(request):
    return render(request, "index.html")


# 客户管理
def client_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["clientname__contains"] = search

    queryset = models.Client.objects.filter(**data_dict).order_by('-clientname')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 5)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)

    # queryset = models.Client.objects.all()
    return render(request, "client/client_list.html", {"queryset": queryset, "search": search})


class ClientModelForm(forms.ModelForm):
    clientno = forms.CharField(min_length=10, max_length=10, label="客户编号")
    clientname = forms.CharField(label="客户名称",
                                 validators=[
                                     RegexValidator(
                                         r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                         '请输入正确的名称')])
    clientstreet = forms.CharField(label="客户所在街道", required=False,
                                   validators=[
                                       RegexValidator(
                                           r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                           '请输入正确的街道')])
    clientcity = forms.CharField(label="客户所在城市",
                                 validators=[
                                     RegexValidator(
                                         r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                         '请输入正确的城市')])
    clientstate = forms.CharField(label="客户所在省(区、市)",
                                  validators=[
                                      RegexValidator(
                                          r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                          '请输入正确的省(区、市)')])
    clientzipcode = forms.CharField(label="客户邮编",
                                    validators=[
                                        RegexValidator(
                                            r'^[0-9]\d{5}$',
                                            '请输入正确的邮编')])
    clienttelno = forms.CharField(label="客户电话",
                                  validators=[
                                      RegexValidator(
                                          r'^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9['
                                          r'1|8|9]))\d{8}$',
                                          '格式错误，请输入正确的电话')])
    clientfaxno = forms.CharField(label="客户传真", required=False,
                                  validators=[
                                      RegexValidator(
                                          r'^(\d{3,4}-)?\d{7,8}$',
                                          '格式错误，请输入正确的传真')])
    clientwebaddress = forms.CharField(label="客户网址", required=False,
                                       validators=[
                                           RegexValidator(
                                               r'^((https?|ftp|file):\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$',
                                               '请输入正确的网址')])

    contactname = forms.CharField(label="联系人姓名",
                                  validators=[
                                      RegexValidator(
                                          r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                          '请输入正确的姓名')])

    contacttelno = forms.CharField(label="联系人电话",
                                   validators=[
                                       RegexValidator(
                                           r'^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9['
                                           r'1|8|9]))\d{8}$',
                                           '格式错误，请输入正确的手机号')])
    contactfaxno = forms.CharField(label="联系人传真", required=False,
                                   validators=[
                                       RegexValidator(
                                           r'^(\d{3,4}-)?\d{7,8}$',
                                           '格式错误，请输入正确的传真')])
    clientemaliaddress = forms.CharField(label="联系人邮箱", required=False,
                                         validators=[
                                             RegexValidator(r'^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$',
                                                            '格式错误，请输入正确的邮箱')])

    #
    class Meta:
        model = models.Client
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_name(self):
        txt_clientno = self.cleaned_data['clientno']
        if models.Client.objects.filter(clientno=txt_clientno).exists():
            raise ValidationError('客户编号已存在')
        return txt_clientno


def client_add(request):
    if request.method == "GET":
        form = ClientModelForm()
        return render(request, 'client/client_add.html', {'form': form})
    # 数据校验
    form = ClientModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/client/list/")
    else:
        return render(request, 'client/client_add.html', {'form': form})


class ClientEditModelForm(ClientModelForm):

    def clean_name(self):
        txt_clientno = self.cleaned_data['clientno']
        if models.Client.objects.exclude(clientno=self.instance.pk).filter(clientno=txt_clientno).exists():
            raise ValidationError('客户编号已存在')
        return txt_clientno


def client_edit(request, no):
    # 获取对象
    row_object = models.Client.objects.filter(clientno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = ClientModelForm(instance=row_object)
        return render(request, 'client/client_edit.html', {'form': form})

    # 实例化当前行
    form = ClientEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/client/list/")
    else:
        return render(request, 'client/client_edit.html', {'form': form})


def client_delete(request):
    no = request.GET.get('no')

    models.Client.objects.filter(clientno=no).delete()

    return redirect('/client/list/')


# 雇员管理
def employee_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["firstname__contains"] = search

    queryset = models.Employee.objects.filter(**data_dict).order_by('-firstname')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 10)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)

    # queryset = models.Employee.objects.all()
    return render(request, "employee/employee_list.html", {"queryset": queryset, "search": search})


class EmployeeModelForm(forms.ModelForm):
    employeeno = forms.CharField(min_length=10, max_length=10, label="雇员编号")
    titleno = forms.CharField(min_length=10, max_length=10, label="职称编号")
    firstname = forms.CharField(label="姓名",
                                validators=[
                                    RegexValidator(
                                        r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                        '请输入正确的姓名')])
    worktelno = forms.CharField(label="电话",
                                validators=[
                                    RegexValidator(
                                        r'^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9['
                                        r'1|8|9]))\d{8}$',
                                        '格式错误，请输入正确的电话')])
    empemailaddress = forms.CharField(label="邮箱",
                                      validators=[
                                          RegexValidator(r'^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$',
                                                         '格式错误，请输入正确的邮箱')])
    socialscuritynumber = forms.CharField(label="身份证号",
                                          validators=[
                                              RegexValidator(
                                                  r'^([1-6][1-9]|50)\d{4}(18|19|20)\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$',
                                                  '格式错误，请输入正确的身份证号')])

    class Meta:
        model = models.Employee
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_employeeno(self):
        txt_employeeno = self.cleaned_data['employeeno']
        if models.Employee.objects.filter(employeeno=txt_employeeno).exists():
            raise ValidationError('雇员编号已存在')
        return txt_employeeno


def employee_add(request):
    if request.method == "GET":
        form = EmployeeModelForm()
        return render(request, 'employee/employee_add.html', {'form': form})
    # 数据校验
    form = EmployeeModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/employee/list/")
    else:
        return render(request, 'employee/employee_add.html', {'form': form})


class EmployeeEditModelForm(EmployeeModelForm):

    def clean_employeeno(self):
        txt_employeeno = self.cleaned_data['employeeno']
        if models.Employee.objects.exclude(employeeno=self.instance.pk).filter(employeeno=txt_employeeno).exists():
            raise ValidationError('雇员编号已存在')
        return txt_employeeno


def employee_edit(request, no):
    # 获取对象
    row_object = models.Employee.objects.filter(employeeno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = EmployeeModelForm(instance=row_object)
        return render(request, 'employee/employee_edit.html', {'form': form})

    # 实例化当前行
    form = EmployeeEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/employee/list/")
    else:
        return render(request, 'employee/employee_edit.html', {'form': form})


def employee_delete(request):
    no = request.GET.get('no')

    models.Employee.objects.filter(employee=no).delete()

    return redirect('/employee/list/')


# 部门管理
def outlet_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["outletno__contains"] = search

    queryset = models.Outlet.objects.filter(**data_dict).order_by('-outletno')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 10)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)
    #  queryset = models.Outlet.objects.all()
    return render(request, "outlet/outlet_list.html", {"queryset": queryset, "search": search})


class OutletModelForm(forms.ModelForm):
    outletno = forms.CharField(min_length=10, max_length=10, label="门店编号")
    outletstreet = forms.CharField(label="门店所在街道", required=False,
                                   validators=[
                                       RegexValidator(
                                           r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                           '请输入正确的街道')])
    outletcity = forms.CharField(label="门店所在城市",
                                 validators=[
                                     RegexValidator(
                                         r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                         '请输入正确的城市')])
    outletstate = forms.CharField(label="门店所在省(区、市)",
                                  validators=[
                                      RegexValidator(
                                          r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                          '请输入正确的省(区、市)')])
    outletzipcode = forms.CharField(label="门店邮编",
                                    validators=[
                                        RegexValidator(
                                            r'^[0-9]\d{5}$',
                                            '请输入正确的邮编')])
    outlettelno = forms.CharField(label="门店电话",
                                  validators=[
                                      RegexValidator(
                                          r'^(?:(?:\+|00)86)?1(?:(?:3[\d])|(?:4[5-7|9])|(?:5[0-3|5-9])|(?:6[5-7])|(?:7[0-8])|(?:8[\d])|(?:9['
                                          r'1|8|9]))\d{8}$',
                                          '格式错误，请输入正确的电话')])
    outletfaxno = forms.CharField(label="门店传真", required=False,
                                  validators=[
                                      RegexValidator(
                                          r'^(\d{3,4}-)?\d{7,8}$',
                                          '格式错误，请输入正确的传真')])

    class Meta:
        model = models.Outlet
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_outletno(self):
        txt_outletno = self.cleaned_data['outletno']
        if models.Outlet.objects.filter(outletno=txt_outletno).exists():
            raise ValidationError('门店编号已存在')
        return txt_outletno


def outlet_add(request):
    if request.method == "GET":
        form = OutletModelForm()
        return render(request, 'outlet/outlet_add.html', {'form': form})
    # 数据校验
    form = OutletModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/outlet/list/")
    else:
        return render(request, 'outlet/outlet_add.html', {'form': form})


class OutletEditModelForm(OutletModelForm):

    def clean_outletno(self):
        txt_outletno = self.cleaned_data['outletno']
        if models.Outlet.objects.exclude(outletno=self.instance.pk).filter(outletno=txt_outletno).exists():
            raise ValidationError('门店编号已存在')
        return txt_outletno


def outlet_edit(request, no):
    # 获取对象
    row_object = models.Outlet.objects.filter(outletno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = OutletModelForm(instance=row_object)
        return render(request, 'outlet/outlet_edit.html', {'form': form})

    # 实例化当前行
    form = OutletEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/outlet/list/")
    else:
        return render(request, 'outlet/outlet_edit.html', {'form': form})


def outlet_delete(request):
    no = request.GET.get('no')

    models.Outlet.objects.filter(outletno=no).delete()

    return redirect('/outlet/list/')


class ManagerModelForm(forms.ModelForm):
    class Meta:
        model = models.Outletmanager
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_outletno(self):
        txt_managerno = self.cleaned_data['managerno']
        if models.Outletmanager.objects.filter(managerno=txt_outletno).exists():
            raise ValidationError('记录已存在')
        return txt_outletno



def outlet_manager(request, no):
    # 获取对象
    row_object = models.Outlet.objects.filter(outletno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = FaultModelForm(instance=row_object)
        return render(request, 'outlet/outlet_edit.html', {'form': form})

    # 实例化当前行
    form = OutletModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/outlet/list/")
    else:
        return render(request, 'outlet/outlet_edit.html', {'form': form})


# 租凭管理
def rental_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["rentalno__contains"] = search

    queryset = models.Rentalagreement.objects.filter(**data_dict).order_by('-rentalno')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 10)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)
    # queryset = models.Rentalagreement.objects.all()
    return render(request, "rental/rental_list.html", {"queryset": queryset})


class RentalModelForm(forms.ModelForm):
    rentalno = forms.CharField(min_length=10, max_length=10, label="租凭编号")
    policyno = forms.CharField(label="合同编号", required=False,
                               validators=[
                                   RegexValidator(
                                       r'^ZL\d{10}$',
                                       '格式错误，请输入正确的编号')])

    class Meta:
        model = models.Rentalagreement
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_rentalno(self):
        txt_rentalno = self.cleaned_data['rentalno']
        if models.Rentalagreement.objects.filter(rentalno=txt_rentalno).exists():
            raise ValidationError('租凭编号已存在')
        return txt_rentalno


def rental_add(request):
    if request.method == "GET":
        form = RentalModelForm()
        return render(request, 'rental/rental_add.html', {'form': form})
    # 数据校验
    form = RentalModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/rental/list/")
    else:
        return render(request, 'rental/rental_add.html', {'form': form})


class RentalEditModelForm(RentalModelForm):

    def clean_rentalno(self):
        txt_rentalno = self.cleaned_data['rentalno']
        if models.Rentalagreement.objects.exclude(rentalno=self.instance.pk).filter(rentalno=txt_rentalno).exists():
            raise ValidationError('租凭编号已存在')
        return txt_rentalno


def rental_edit(request, no):
    # 获取对象
    row_object = models.Rentalagreement.objects.filter(rentalno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = RentalModelForm(instance=row_object)
        return render(request, 'rental/rental_edit.html', {'form': form})

    # 实例化当前行
    form = RentalEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/rental/list/")
    else:
        return render(request, 'rental/rental_edit.html', {'form': form})


def rental_delete(request):
    no = request.GET.get('no')

    models.Vehicle.objects.filter(vehlicenseno=no).delete()

    return redirect('/vehicle/list/')


# 故障报告管理
def fault_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["vehlicenseno__contains"] = search

    queryset = models.Faultreport.objects.filter(**data_dict).order_by('-vehlicenseno')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 10)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)
    # queryset = models.Faultreport.objects.all()
    return render(request, "fault/fault_list.html", {"queryset": queryset})


class FaultModelForm(forms.ModelForm):
    faultreportno = forms.CharField(min_length=10, max_length=10, label="车辆编号")

    class Meta:
        model = models.Faultreport
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_faultreportno(self):
        txt_faultreportno = self.cleaned_data['faultreportno']
        if models.Faultreport.objects.filter(faultreportno=txt_faultreportno).exists():
            raise ValidationError('车辆编号已存在')
        return txt_faultreportno


def fault_add(request):
    if request.method == "GET":
        form = FaultModelForm()
        return render(request, 'fault/fault_add.html', {'form': form})
    # 数据校验
    form = FaultModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/fault/list/")
    else:
        return render(request, 'fault/fault_add.html', {'form': form})


class FaultEditModelForm(FaultModelForm):

    def clean_faultreportno(self):
        txt_faultreportno = self.cleaned_data['faultreportno']
        if models.Faultreport.objects.exclude(faultreportno=self.instance.pk).filter(faultreportno=txt_faultreportno).exists():
            raise ValidationError('车辆编号已存在')
        return txt_faultreportno


def fault_edit(request, no):
    # 获取对象
    row_object = models.Faultreport.objects.filter(faultreportno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = FaultModelForm(instance=row_object)
        return render(request, 'fault/fault_edit.html', {'form': form})

    # 实例化当前行
    form = FaultEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/fault/list/")
    else:
        return render(request, 'fault/fault_edit.html', {'form': form})


def fault_delete(request):
    no = request.GET.get('no')

    models.Faultreport.objects.filter(outletno=no).delete()

    return redirect('/fault/list/')


# 车辆信息管理
def vehicle_list(request):
    data_dict = {}
    search = request.GET.get("search", "")

    if search:
        data_dict["vehlicenseno__contains"] = search

    queryset = models.Vehicle.objects.filter(**data_dict).order_by('-vehlicenseno')

    # 每页只显示一行号码
    paginator = Paginator(queryset, 10)
    # 获取url中的号码
    page = request.GET.get('page')
    # 通过组件将页码对应的内容返回给queryset
    queryset = paginator.get_page(page)

    # queryset = models.Vehicle.objects.all()
    return render(request, "vehicle/vehicle_list.html", {"queryset": queryset})


class VehicleModelForm(forms.ModelForm):
    vehlicenseno = forms.CharField(min_length=10, max_length=10, label="车辆编号")
    vehiclemake = forms.CharField(label="制车厂",
                                  validators=[
                                      RegexValidator(
                                          r'^[\u4E00-\u9FA5]{2,20}([\u25CF\u00B7][\u4E00-\u9FA5]{2,20})*$',
                                          '请输入正确的名称')])
    color = forms.CharField(label="颜色",
                            validators=[
                                RegexValidator(
                                    r'^[\u4E00-\u9FA5]{2,10}([\u25CF\u00B7][\u4E00-\u9FA5]{2,10})*$',
                                    '请输入正确的名称')])
    nodoors = forms.CharField(label="车牌号",
                              validators=[
                                  RegexValidator(
                                      r'^[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤青藏川宁琼]{1}[A-HJ-NP-Z]{1}(([A-HJ-NP-Z0-9]{5})|([0-9]{6}|[A-HJ-NP-Z]{1}[0-9]{5}|[0-9]{5}[A-HJ-NP-Z]{1}|[A-HJ-NP-Z]{2}[0-9]{4}))$',
                                      '请输入正确的车牌号')])

    class Meta:
        model = models.Vehicle
        fields = "__all__"

    # 给元素添加样式
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的组件，添加form-control样式
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_vehlicenseno(self):
        txt_vehlicenseno = self.cleaned_data['vehlicenseno']
        if models.Vehicle.objects.filter(vehlicenseno=txt_vehlicenseno).exists():
            raise ValidationError('车辆编号已存在')
        return txt_vehlicenseno


def vehicle_add(request):
    if request.method == "GET":
        form = VehicleModelForm()
        return render(request, 'vehicle/vehicle_add.html', {'form': form})
    # 数据校验
    form = VehicleModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        return redirect("/vehicle/list/")
    else:
        return render(request, 'vehicle/vehicle_add.html', {'form': form})


class VehicleEditModelForm(VehicleModelForm):
    def clean_vehlicenseno(self):
        txt_vehlicenseno = self.cleaned_data['vehlicenseno']
        if models.Vehicle.objects.exclude(vehlicenseno=self.instance.pk).filter(vehlicenseno=txt_vehlicenseno).exists():
            raise ValidationError('车辆编号已存在')
        return txt_vehlicenseno


def vehicle_edit(request, no):
    # 获取对象
    row_object = models.Vehicle.objects.filter(vehlicenseno=no).first()

    if request.method == "GET":
        # 对象设置为form
        form = VehicleModelForm(instance=row_object)
        return render(request, 'vehicle/vehicle_edit.html', {'form': form})

    # 实例化当前行
    form = VehicleEditModelForm(data=request.POST, instance=row_object)

    # 数据校验
    if form.is_valid():
        form.save()
        return redirect("/vehicle/list/")
    else:
        return render(request, 'vehicle/vehicle_edit.html', {'form': form})


def vehicle_delete(request):
    no = request.GET.get('no')

    models.Vehicle.objects.filter(vehlicenseno=no).delete()

    return redirect('/vehicle/list/')


# 图表

def chart_bar(request):
    clientnum = models.Client.objects.count()
    employeenum = models.Employee.objects.count()
    faultreportnum = models.Faultreport.objects.count()
    outletnum = models.Outlet.objects.count()
    rentalnum = models.Rentalagreement.objects.count()
    vehiclenum = models.Vehicle.objects.count()

    legend = ['数量']
    x_axis = ['客户', '门店', '雇员', '车辆', '检修记录', '合同']
    series_list = [
        {
            "name": "数量",
            "type": 'bar',
            "data": [clientnum, outletnum, employeenum, vehiclenum, faultreportnum, rentalnum]
        }
    ]

    result = {
        "status": True,
        "data": {
            'legend': legend,
            'series_list': series_list,
            'x_axis': x_axis,
        }
    }

    return JsonResponse(result)


def chart_pie(request):
    data = models.Client.objects.values('clientstate').distinct()
    series_data = []
    for obj in data:
        item_state = obj['clientstate']
        num = models.Client.objects.filter(clientstate=item_state).count()
        series_data.append({"value": num, "name": item_state})
    result = {
        "status": True,
        "data": {
            'series_list': series_data,
        }
    }
    return JsonResponse(result)


def chart_map(request):
    data = models.Outlet.objects.values('outletcity').distinct()
    print(data)
    series_data = []
    for obj in data:
        item_state = obj['outletcity']
        num = models.Outlet.objects.filter(outletcity=item_state).count()
        series_data.append({"name": item_state, "value": num})

    print(series_data)
    result = {
        "status": True,
        "data": {
            'series_list': series_data,
        }
    }
    return JsonResponse(result)