# Question 2
# Kwan Hau Thomas, LEE (1650501)

# library
import pandas as pd

# import data
df = pd.DataFrame({
    'Outlook': ['Sun', 'Sun', 'Cloud', 'Rain', 'Rain', 'Rain', 'Cloud', 'Sun', 'Sun', 'Rain', 'Sun', 'Cloud', 'Cloud', 'Rain'],
    'Temp': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    'Tennis?': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No' ]
})

# a) priors
prob = float(len(df[df['Tennis?'] == 'Yes'])) / len(df)
print('P(Tennis? == Yes) = %.4f' % prob)

prob = float(len(df[df['Tennis?'] == 'No'])) / len(df)
print('P(Tennis? == No) = %.4f' % prob)

# b) vnb
v = {col: df[col].unique() for col in list(df) if col == 'Tennis?'}

a = {
    'Outlook': 'Cloud',
    'Temp': 'Mild',
    'Humidity': 'Normal',
    'Wind': 'Weak'
}


probs = []
prob_desc = []

# for all possible value of prior probabilities
for prior in v:
    for prior_v in v[prior]:
        prob = float(len(df[df[prior] == prior_v])) / len(df)
        # for all forecast for tomorrow
        for key in a:
            likelihood = float(len(df[(df[prior] == prior_v) & (df[key] == a[key])])) / len(df[df[prior] == prior_v])
            print 'P(%s == %s | %s == %s) = %.4f' % (key, a[key], prior, prior_v, likelihood)
            prob *= likelihood
        prob_desc.append('P(%s == %s)' % (prior, prior_v))
        probs.append(prob)

print prob_desc
print probs
# normalised
norm_probs = [p / sum(probs) for p in probs]
print norm_probs