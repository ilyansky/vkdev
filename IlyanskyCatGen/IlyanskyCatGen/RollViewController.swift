import UIKit

class RollViewController: UIViewController {
    @IBOutlet weak var rollButton: UIButton!
    @IBOutlet weak var catNameTextField: UITextField!
    @IBOutlet weak var rollActivityIndicator: UIActivityIndicatorView!

    override func viewDidLoad() {
        super.viewDidLoad()
        rollActivityIndicator.style = .large
        rollActivityIndicator.isHidden = true
        
        let tap = UITapGestureRecognizer(target: self, action: #selector(UIInputViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
    }
    
    @objc func dismissKeyboard() {
        view.endEditing(true)
    }
    
    @IBAction func tapRollButton(_ sender: Any) {
        fetchCat { [weak self] data in
            let sb = UIStoryboard(name: "Main", bundle: nil)
            let vc = sb.instantiateViewController(withIdentifier: "CatImageViewController") as? CatImageViewController
            vc?.modalTransitionStyle = .crossDissolve
            
            let name = self?.catNameTextField.text?.uppercased()
            vc?.catName = name == "" ? "BARSIK" : name
            vc?.catImage = UIImage(data: data)
            
            self?.navigationController?.pushViewController(vc!, animated: true)
            self?.turnOffRollButtonIf(false)
        }
    }
    
    private func fetchCat(completion: @escaping (Data) -> Void) {
        guard let url = URL(string: "https://cataas.com/cat") else { return }
        
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

