stre = '((Points.id > fdsf) & (Points.id > fdsf) | )(Points.id > ffd) | (Points.id > ffd) '

def transform_str(resArr):
    if '| )' in resArr:
        resArr = resArr.replace(' | )', ') | ')
    if '& )' in resArr:
        resArr = resArr.replace(' & )', ') & ')
    return resArr
