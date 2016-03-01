# Prostate-Cancer-Dream-Challenge
Team: Data Wizard

**** For Challenge 1a ****

Environment : Linux、Windows 7
Language : Python( Version 2.7.10 )，R studio
Packages need to be installed: 
	→ Python : pandas、sklearn、Orange
	→ R : survival , timeROC , ROCR , survivalMPL , plyr , caret , discretization , FSelector

Steps:
1. Please change paths of the input files of code if need.
2. Run the “preprocess.py. ” to preprocess the datasets
→ $python preprocess.py
Input : CoreTable_training.csv ,CoreTable_leaderboard.csv

Output : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
3. Run the “Final.R” to bin some features.

Input : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
Output : Train1.csv, Train2.csv,  Train3.csv, Test1.csv, Test2.csv, Test3.csv
4. Run the “featureq1a.py” 
→ $python featureq1a.py
Input : Train1.csv, Train2.csv,  Train3.csv, Test1.csv, Test2.csv, Test3.csv
Output : Train_after1.csv, Train2_ after.csv,  Train3_ after.csv, Test1_ after.csv, Test2_ after.csv, Test3_ after.csv

5. Run the “Cmodel.R” to fit cox_mpl model

Input : Train_after1.csv, Train2_ after.csv,  Train3_ after.csv, Test1_ after.csv, Test2_ after.csv, Test3_ after.csv
Output : Q1A.csv

-----------------------------------------------------------------------------------------------------------------------------
**** For Challenge 1b ****

Environment : Linux、Windows 7
Language : Python( Version 2.7.10 )，R studio
Packages need to be installed: 
	→ Python : pandas、sklearn、Orange
	→ R : survival , timeROC , ROCR , survivalMPL , plyr , caret , discretization , FSelector

Steps:
1. Please change paths of the input files of code if need.
2. Run the “preprocess.py. ” to preprocess the datasets
→ $python preprocess.py
Input : CoreTable_training.csv ,CoreTable_leaderboard.csv

Output : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
3. Run the “Q1b.R” to bin some features.
→ $ Rscript Q1b.R 
Input : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
Output : test_Q1b.csv, training_Q1b.csv
4. Run the “final_read_index_q1b.py” 
→ $python final_read_index_q1b.py
Input : test_Q1b.csv, training_Q1b.csv
Output: result.

-----------------------------------------------------------------------------------------------------------------------------
**** For Challenge 2a ****

Environment : Linux、Windows 7
Language : Python( Version 2.7.10 )，R studio
Packages need to be installed: 
	→ Python : pandas、sklearn、Orange
	→ R : survival , timeROC , ROCR , survivalMPL , plyr , caret , discretization , FSelector

Steps:
1. Please change paths of the input files of code if need.
2. Run the “preprocess.py. ” to preprocess the datasets
→ $python preprocess.py
Input : CoreTable_training.csv ,CoreTable_leaderboard.csv

Output : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
3. Run the “Final.R” to bin some features.
Input : acs.csv, gelg.csv , ven.csv, and CoreTable_leaderboard_new.csv
Output : TrainAll.csv, TestAll.csv
4. Run the “featureq2.py” 
→ $python featureq2.py
Input : TrainAll.csv, TestAll.csv
Output : Train_afterAll.csv, Test_ afterAll.csv

5. Run the “final_q2.py” 
→ $python final_q2.py
Input : Train_afterAll.csv, Test_ afterAll.csv 
Output: result
