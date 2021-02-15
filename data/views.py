from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from .models import Htf, Drug
from django.contrib import messages
import csv, io
from django.core.paginator import Paginator
from .filters import Htffilter

# Create your views here.

# From data/urls.py
# Views = webpages
# Each function defines what to do when the url referenced in data/urls.py
# is accessed with a http request
# In these examples, each request to the function returns an httpResponse
# these are wrapped in <h1></h1> tags, meaning page headers
# Route is as follows:
# htf_web/urls.py -> data/urls.py -> views.py


# def home(request):
    # define the function to deal with home receiving a request
    # return HttpResponse("<h1>Home</h1>")
    # A request returns a HTTPResponse

def home(request):
    # Define function, what to do when a request comes
    return render(request, "data/home.html", {'title': 'The Human Transcription Factor Database'})
    # return render of template located in data/templates/data/home.html

def htf(request):
    all_htfs = Htf.objects.all().order_by('gene_name')

    paginator = Paginator(all_htfs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Add a dictionary containing htf's, can now display on html page
    return render(request, "data/htf.html", {'page_obj': page_obj, 'title': 'HTF Search'})

def detail(request, gene_name):
    htf = Htf.objects.get(gene_name=gene_name)
    context={
        "htf":htf
    }
    return render(request, "data/details.html", context)

def drug(request):
    return render(request, "data/drug.html", {'title': 'Drug Search'})

def genexp(request):
    return render(request, "data/genexp.html", {'title': 'GEO DataSet Analyser'})

def download(request):
    return render(request, "data/download.html", {'title': 'Download'})

def about(request):
    return render(request, "data/about.html", {'title': 'About'})

def help(request):
    return render(request, "data/help.html", {'title': 'Help'})

def documentation(request):
    return render(request, "data/documentation.html", {'title': 'Documentation'})


def search(request):
    fil = Htffilter(request.GET, queryset=Htf.objects.all())
    if request.method == "GET":
        search = request.GET.get("q")
        f = Htffilter(request.GET, queryset=Htf.objects.filter(
            Q(chromosome_name__icontains=search) | Q(dbd__icontains=search)
            | Q(ensemble_id__icontains=search)
            | Q(function__icontains=search) | Q(gene_end__icontains=search)
            | Q(gene_name__icontains=search) | Q(gene_start__icontains=search)
            | Q(id__icontains=search) | Q(prot_name__icontains=search)
            | Q(strand__icontains=search) | Q(sub_cell_location__icontains=search)
            | Q(uniprot_id__icontains=search)
        ))
        paginator = Paginator(f.qs, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        new_request = ''
        for i in request.GET:
            if i != 'page':
                val = request.GET.get(i)
                new_request += f"&{i}={val}"

    return render(request, "data/search.html", {'filter': fil, 'page_obj':page_obj,'new_request': new_request})


def data_upload(request):
    data = Htf.objects.all()
    prompt = {
        "Order": "Order of the CSV should be:"
                 "Ensemble ID, DBD, Gene name, Chromosome/scaffold name, "
                 "Gene start (bp), Gene end (bp), Strand, "
                 "UniProt ID, Protein names, Function [CC], Subcellular location [CC]"
    }
    if request.method=="GET":
        return render(request, "data/data_upload.html", prompt)

    csv_file = request.FILES["file"]

    if not csv_file.name.endswith(".csv"):
        messages.error(request, "This is not a .csv file")

    data_set = csv_file.read().decode("UTF-8")

    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter='\t', quotechar="|"):
        _, created = Htf.objects.update_or_create(
            ensemble_id=column[0],
            dbd=column[1],
            gene_name=column[2],
            chromosome_name=column[3],
            gene_start=column[4],
            gene_end = column[5],
            strand = column[6],
            uniprot_id = column[7],
            prot_name = column[8],
            function = column[9],
            sub_cell_location=column[10]
        )
    context = {}
    return render(request, "data/data_upload.html", context)
