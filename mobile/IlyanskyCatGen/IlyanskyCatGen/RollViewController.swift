import UIKit
//import Foundation

class RollViewController: UIViewController {
    @IBOutlet weak var rollButton: UIButton!
    @IBOutlet weak var catNameTextField: UITextField!
    @IBOutlet weak var rollActivityIndicator: UIActivityIndicatorView!
    @IBOutlet weak var scrollView: UIScrollView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        rollActivityIndicator.style = .large
        rollActivityIndicator.isHidden = true
        
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillShow(notification:)), name: UIResponder.keyboardWillShowNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(keyboardWillHide(notification:)), name: UIResponder.keyboardWillHideNotification, object: nil)
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
    @objc
    private func keyboardWillShow(notification: NSNotification) {
       let keyboardHeight = (notification.userInfo![UIResponder.keyboardFrameEndUserInfoKey] as! NSValue).cgRectValue.height

        scrollView.contentInset = UIEdgeInsets(top: 0, left: 0, bottom: keyboardHeight, right: 0)
        
    }

    @objc
    private func keyboardWillHide(notification: NSNotification) {
       let keyboardHeight = (notification.userInfo![UIResponder.keyboardFrameEndUserInfoKey] as! NSValue).cgRectValue.height
        
        scrollView.contentInset = UIEdgeInsets(top: 0, left: 0, bottom: keyboardHeight, right: 0)
    }
    
    @IBAction func tapRollButton(_ sender: Any) {
        let name = catNameTextField.text?.uppercased() ?? ""
                
        fetchCat(text: name == "" ? "BARSIK" : name) { [weak self] data in
            let sb = UIStoryboard(name: "Main", bundle: nil)
            let vc = sb.instantiateViewController(withIdentifier: "CatImageViewController") as? CatImageViewController
            vc?.modalTransitionStyle = .crossDissolve
            
            vc?.catName = name == "" ? "BARSIK" : name
            vc?.catImage = UIImage(data: data)
            
            self?.navigationController?.pushViewController(vc!, animated: true)
            self?.turnOffRollButtonIf(false)
        }
    }
    
    private func fetchCat(text: String, completion: @escaping (Data) -> Void) {
        guard let url = URL(string: "https://cataas.com/cat/says/\(text)?fontSize=50&fontColor=white") else { return }

        turnOffRollButtonIf(true)
        
        let task = URLSession.shared.dataTask(with: url) { data, error, response in
            guard let data = data, error != nil else {
                return
            }
            
            DispatchQueue.main.async {
                completion(data)
            }
        }
        task.resume()
    }
    
    private func turnOffRollButtonIf(_ flag: Bool) {
        if flag {
            rollButton.setTitle("", for: .normal)
            rollButton.isUserInteractionEnabled = false
            
            rollActivityIndicator.isHidden = false
            rollActivityIndicator.startAnimating()
        } else {
            rollActivityIndicator.stopAnimating()
            rollActivityIndicator.isHidden = true
            
            rollButton.setTitle("ROLL", for: .normal)
            rollButton.isUserInteractionEnabled = true
        }
    }
    
}

