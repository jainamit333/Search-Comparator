from flask import Flask, render_template, request

from File_Loader import file_from_url, add_data_to_result_to_show, scoop_json, convert_list_to_dic_and_filter, \
    elements_of_same_instance , load_file_from_upload

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/searchcomparebatch',methods=['POST'])
def batch_search_comparator():
    print "start batch file"
    data = load_file_from_upload(request.files['batch'])
    url1 = data['host1']+'/international/json/listing/'+data['lob1']
    url2 = data['host2']+'/international/json/listing/'+data['lob2']
    case_wise_result_to_show = {}
    case_wise_recommandation_wise_result = {}
    case_wise_attribute_difference_recommendation_wise = {}
    attribute_difference_recommendation_nested = {}
    for case in data['cases']:
        case_string = "/"+case['trip']+"/"+case['date']+"/"+case['pax']+"/"+case['lastval']
        old_url = url1+case_string
        new_url = url2+case_string

        result_to_show = []
        recommandation_wise_result = {}
        attribute_difference_recommendation_wise = {}
        attribute_difference_recommendation_wise_nested = {}
        case_wise_result_to_show[case_string] = result_to_show
        case_wise_recommandation_wise_result[case_string]= recommandation_wise_result
        case_wise_attribute_difference_recommendation_wise[case_string] = attribute_difference_recommendation_wise
        attribute_difference_recommendation_nested[case_string] = attribute_difference_recommendation_wise_nested

        # load Files From Url
        old_json = file_from_url(old_url)
        new_json = file_from_url(new_url)
        if old_json == "Connection Error":
            add_data_to_result_to_show(result_to_show, "Error while uploading File 1")
            continue
            #return render_template('result.html', data=result_to_show,data2 = recommandation_wise_result,data3 = attribute_difference_recommendation_wise)
        if new_json == "Connection Error":
            add_data_to_result_to_show(result_to_show, "Error while uploading File 2")
            continue
            #return render_template('result.html', data=result_to_show,data2 = recommandation_wise_result,data3 = attribute_difference_recommendation_wise)

        old_json = scoop_json(old_json, 0, "results")
        new_json = scoop_json(new_json, 0, "results")

        add_data_to_result_to_show(result_to_show, 'Length of results in File 1 without filter ' + str(len(old_json)))
        add_data_to_result_to_show(result_to_show, 'Length of results in File 2 without filter ' + str(len(new_json)))

        # create dictionary and filter according to airline
        services = request.form['service']
        old_dictionary = convert_list_to_dic_and_filter(old_json, request.form['dictionary_id_1'],
                                                    "REM_AFTER_LAST_UNDERSCORE", services)
        new_dictionary = convert_list_to_dic_and_filter(new_json, request.form['dictionary_id_2'],
                                                    "REM_AFTER_LAST_UNDERSCORE", services)

        old_json = None
        new_json = None

        add_data_to_result_to_show(result_to_show, 'Length of results in File 1 after filter ' + str(len(old_dictionary)))
        add_data_to_result_to_show(result_to_show, 'Length of results in File 2 after filter ' + str(len(new_dictionary)))


        if not isinstance(old_dictionary, dict):
            add_data_to_result_to_show(result_to_show, "Unable to convert dictionary for file 1 , Internal Error")
            continue
            #return render_template("result.html", data=result_to_show,data2 = recommandation_wise_result,data3=attribute_difference_recommendation_wise)
        if not isinstance(new_dictionary, dict):
            add_data_to_result_to_show(result_to_show, "Unable to convert dictionary for file 2 , Internal Error")
            continue
            #return render_template("result.html", data=result_to_show,data2 = recommandation_wise_result,data3=attribute_difference_recommendation_wise)

        start_compare_recommendations_dictionary(old_dictionary, new_dictionary, result_to_show, recommandation_wise_result,attribute_difference_recommendation_wise,attribute_difference_recommendation_wise_nested)


    return render_template('result.html', data=case_wise_result_to_show,data2 = case_wise_recommandation_wise_result,
                           data3 = case_wise_attribute_difference_recommendation_wise,data4 = attribute_difference_recommendation_nested)



@app.route('/searchcompare',methods=['POST'])
def search_comparator():
    print("Start Search Comparator")
    result_to_show = []
    recommandation_wise_result = {}
    attribute_difference_recommendation_wise_level1 = {}
    attribute_difference_recommendation_nested = {}

    # load Files From Url
    old_json = file_from_url(request.form['old_url'])
    new_json = file_from_url(request.form['new_url'])
    if old_json == "Connection Error":
        add_data_to_result_to_show(result_to_show, "Error while uploading File 1")
        return render_template('singleresult.html', data=result_to_show,data2 = recommandation_wise_result,data3 = attribute_difference_recommendation_wise_level1)
    if new_json == "Connection Error":
        add_data_to_result_to_show(result_to_show, "Error while uploading File 2")
        return render_template('singleresult.html', data=result_to_show,data2 = recommandation_wise_result,data3 = attribute_difference_recommendation_wise_level1)

    if isinstance(old_json,dict):
        old_json = scoop_json(old_json, -1, "recommendations.results")
    else:
        old_json = scoop_json(old_json, 0, "results")

    if isinstance(new_json,dict):
        new_json = scoop_json(new_json, -1, "recommendations.results")
    else:
        new_json = scoop_json(new_json, 0, "results")

    add_data_to_result_to_show(result_to_show, 'Length of results in File 1 without filter ' + str(len(old_json)))
    add_data_to_result_to_show(result_to_show, 'Length of results in File 2 without filter ' + str(len(new_json)))

    # create dictionary and filter according to airline
    services = request.form['service']
    old_dictionary = convert_list_to_dic_and_filter(old_json, request.form['dictionary_id_1'],
                                                    "REM_AFTER_LAST_UNDERSCORE", services)
    new_dictionary = convert_list_to_dic_and_filter(new_json, request.form['dictionary_id_2'],
                                                    "REM_AFTER_LAST_UNDERSCORE", services)

    old_json = None
    new_json = None

    add_data_to_result_to_show(result_to_show, 'Length of results in File 1 after filter ' + str(len(old_dictionary)))
    add_data_to_result_to_show(result_to_show, 'Length of results in File 2 after filter ' + str(len(new_dictionary)))


    if not isinstance(old_dictionary, dict):
        add_data_to_result_to_show(result_to_show, "Unable to convert dictionary for file 1 , Internal Error")
        return render_template("singleresult.html", data=result_to_show,data2 = recommandation_wise_result,data3=attribute_difference_recommendation_wise_level1)
    if not isinstance(new_dictionary, dict):
        add_data_to_result_to_show(result_to_show, "Unable to convert dictionary for file 2 , Internal Error")
        return render_template("singleresult.html", data=result_to_show,data2 = recommandation_wise_result,data3=attribute_difference_recommendation_wise_level1)

    start_compare_recommendations_dictionary(old_dictionary, new_dictionary, result_to_show, recommandation_wise_result,attribute_difference_recommendation_wise_level1,attribute_difference_recommendation_nested)
    return render_template('singleresult.html', data=result_to_show,data2 = recommandation_wise_result,data3 = attribute_difference_recommendation_wise_level1,data4 =attribute_difference_recommendation_nested)



# noinspection PyBroadException
def compute_defference_in_attributes(old_data, new_data, difference_in_reccomendation_list):
    difference_in_reccomendation_list.append(set(old_data.keys()) - set(new_data.keys()))
    difference_in_reccomendation_list.append(set(new_data.keys()) - set(old_data.keys()))



def start_compare_recommendations_dictionary(old_dictionary, new_dictionary, result_to_show, recommandation_wise_result,
                                             attribute_difference_recommendation_wise,attribute_difference_recommendation_nested):
    # loop the dictionary
    for key_attr in old_dictionary:
        recommendation_list = []
        difference_in_reccomendation_list = []
        difference_in_reccomendation_list_nested = []
        recommandation_wise_result[key_attr] = recommendation_list
        attribute_difference_recommendation_wise[key_attr] = difference_in_reccomendation_list
        attribute_difference_recommendation_nested[key_attr] = difference_in_reccomendation_list_nested
        try:
            new_data = new_dictionary[key_attr]
        except Exception:
            add_data_to_result_to_show(recommendation_list, "Reccomendation not found in File 2 for key" + key_attr)
            continue
        old_data = old_dictionary[key_attr]
        compute_defference_in_attributes(old_data,new_data,difference_in_reccomendation_list)
        compare_recommendation(old_data, new_data, recommendation_list, key_attr,difference_in_reccomendation_list_nested)


def compare_recommendation(recommendation_old, recommendation_new, result_to_show, ket_attr,difference_in_reccomendation_list_nested):

    if elements_of_same_instance(recommendation_old, recommendation_new):

        if isinstance(recommendation_new, dict):
            compare_dict_value(recommendation_old,recommendation_new,result_to_show,ket_attr,"",difference_in_reccomendation_list_nested)
        elif isinstance(recommendation_new, (list, set)):

            compare_list_values(recommendation_old, recommendation_new, result_to_show, ket_attr, ""),difference_in_reccomendation_list_nested
        elif isinstance(recommendation_new, (str, int, float, bool,unicode)):

            compare_single_value(recommendation_old, recommendation_new, result_to_show, ket_attr, ket_attr,difference_in_reccomendation_list_nested)

    else:
        add_data_to_result_to_show(result_to_show, "Recommendation is not of same type insatance for key " + ket_attr)


def compare_single_value(recommendation_old, recommendation_new, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested):

    if not recommendation_old == recommendation_new:
        print "Value does not match"
        add_data_to_result_to_show(result_to_show,
                                   "Value does not match in Recommendation " + str(ket_attr) + " Attribute Name " +
                                   current_attribute_name+" with values :---- "+str(recommendation_old)+" -----  "+str(recommendation_new))


def compare_unknown_element(old_data, new_data, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested):
    if elements_of_same_instance(old_data, new_data):
        print "start comparing"

        if isinstance(old_data, dict):
            print "start dic comparision"
            compare_dict_value(old_data,new_data,result_to_show,ket_attr,current_attribute_name,difference_in_reccomendation_list_nested)
        elif isinstance(old_data, (list, set)):
            print "comapre list or set"
            compare_list_values(old_data, new_data, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested)
        elif isinstance(old_data, (str, int, float, bool,unicode)):
            print "Compare single value"
            compare_single_value(old_data, new_data, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested)
    else:
        add_data_to_result_to_show(result_to_show, "Recommendation is not of same type insatance for key " + ket_attr)


def compare_list_values(list_one, list_two, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested):
    print "start comparing list"
    if not len(list_one) == len(list_two):
        add_data_to_result_to_show(result_to_show,
                                   "Length of List found is not equal for Recommendation " + ket_attr +
                                   " Attribute Name " + current_attribute_name+" value 1 ----"+str(list_one)+"   ----value 2 -------"+str(list_two))
        add_data_to_result_to_show(difference_in_reccomendation_list_nested,"Length of List found is not equal for Recommendation " + ket_attr +
                                   " Attribute Name " + current_attribute_name+" value 1 ----"+str(list_one)+"   ----value 2 -------"+str(list_two))
    else:
        counter = 0
        for old_data in list_one:
            compare_unknown_element(old_data, list_two[counter], result_to_show, ket_attr,
                                    current_attribute_name + ":" + str(counter),difference_in_reccomendation_list_nested)
            counter=counter+1


def compare_dict_value(dict_old, dict_new, result_to_show, ket_attr, current_attribute_name,difference_in_reccomendation_list_nested):
    print "Comparing dictionary value"
    for attribute in dict_old:
        try:
            new_value = dict_new[attribute]
        except:
            add_data_to_result_to_show(result_to_show, "Element not found for Recommendation with key " + ket_attr
                                       + " attribute " + current_attribute_name + attribute)
            add_data_to_result_to_show(difference_in_reccomendation_list_nested, "Element not found for Recommendation with key " + ket_attr
                                       + " attribute " + current_attribute_name + attribute)
        old_value = dict_old[attribute]
        compare_unknown_element(old_value, new_value, result_to_show, ket_attr,current_attribute_name + "." + attribute,difference_in_reccomendation_list_nested)

if __name__ == '__main__':
    app.run(debug=True)